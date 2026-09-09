import secrets
from pathlib import Path

from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    Query,
    UploadFile,
    status,
)
from sqlalchemy.orm import Session
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import ChatService
from app.core.auth import get_current_user
from app.core.database import get_db

from app.models.comment import Comment
from app.models.document import Document
from app.models.share import Share
from app.models.user import User
from app.core.config import settings

from app.schemas.document import (
    CommentCreate,
    CommentResponse,
    DocumentResponse,
    GuestCommentCreate,
    ShareResponse,
)

from app.services.document_store import DocumentStore
from app.services.gemini_service import GeminiService
from app.services.pdf_service import PDFService


router = APIRouter(prefix="/documents", tags=["Documents"])

UPLOAD_DIR = Path(__file__).resolve().parents[3] / "storage" / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# UPLOAD PDF
# ============================================================

@router.post(
    "/upload",
    response_model=DocumentResponse,
    status_code=status.HTTP_201_CREATED,
)
def upload_pdf(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is required.",
        )

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed.",
        )

    safe_name = Path(file.filename).name
    unique_name = f"{secrets.token_hex(16)}_{safe_name}"
    file_path = UPLOAD_DIR / unique_name

    document = None

    try:
        with open(file_path, "wb") as output:
            content = file.file.read()

            if len(content) > PDFService.MAX_FILE_SIZE:
                raise HTTPException(
                    status_code=400,
                    detail="PDF file is too large. Maximum size is 20 MB.",
                )

            output.write(content)

        pdf_service = PDFService()

        # Validate PDF before creating the database record
        reader = pdf_service.validate_pdf(file_path)

        # Create the document object, but DON'T commit yet
        document = Document(
            owner_id=current_user.id,
            filename=safe_name,
            file_path=str(file_path),
        )

        db.add(document)
        db.flush()

        # Extract and index PDF chunks
        chunks = pdf_service.extract_documents(
            reader=reader,
            document_id=document.id,
            owner_id=current_user.id,
            filename=safe_name,
        )

        document_store = DocumentStore()
        document_store.add_documents(chunks)

        # Generate AI summary
        full_text = pdf_service.extract_full_text(reader)
        summary_text = full_text[:50000]

        gemini_service = GeminiService()
        summary = gemini_service.generate_summary(summary_text)

        document.summary = summary

        # Commit ONLY after every processing step succeeds
        db.commit()
        db.refresh(document)

        return document

    except HTTPException:
        db.rollback()

        if file_path.exists():
            file_path.unlink()

        raise

    except Exception as exc:
        db.rollback()

        if file_path.exists():
            file_path.unlink()

        raise HTTPException(
            status_code=500,
            detail=f"PDF processing failed: {str(exc)}",
        ) from exc


# ============================================================
# GET DOCUMENTS / DASHBOARD
# ============================================================

@router.get(
    "",
    response_model=list[DocumentResponse],
)
def get_documents(
    search: str | None = Query(
        default=None,
        description="Search documents by filename",
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = (
        db.query(Document)
        .filter(Document.owner_id == current_user.id)
    )

    if search:
        query = query.filter(
            Document.filename.ilike(f"%{search}%")
        )

    documents = (
        query
        .order_by(Document.created_at.desc())
        .all()
    )

    return documents


# ============================================================
# CREATE SHARE LINK
# ============================================================

@router.post(
    "/{document_id}/share",
    response_model=ShareResponse,
)
def create_share_link(
    document_id: int,
    invited_email: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    document = (
        db.query(Document)
        .filter(
            Document.id == document_id,
            Document.owner_id == current_user.id,
        )
        .first()
    )

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found.",
        )

    token = secrets.token_urlsafe(32)

    share = Share(
        document_id=document.id,
        token=token,
        invited_email=invited_email,
    )

    db.add(share)
    db.commit()
    db.refresh(share)

    share_url = f"{settings.FRONTEND_URL}/shared/{token}"

    return ShareResponse(
        token=share.token,
        invited_email=share.invited_email,
        share_url=share_url,
    )


# ============================================================
# GET SHARED DOCUMENT
# ============================================================

@router.get(
    "/shared/{token}",
    response_model=DocumentResponse,
)
def get_shared_document(
    token: str,
    db: Session = Depends(get_db),
):
    share = (
        db.query(Share)
        .filter(Share.token == token)
        .first()
    )

    if not share:
        raise HTTPException(
            status_code=404,
            detail="Invalid share link.",
        )

    document = (
        db.query(Document)
        .filter(Document.id == share.document_id)
        .first()
    )

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found.",
        )

    return document


# ============================================================
# ADD AUTHENTICATED OWNER COMMENT
# ============================================================

@router.post(
    "/{document_id}/comments",
    response_model=CommentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_comment(
    document_id: int,
    comment_data: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    document = (
        db.query(Document)
        .filter(
            Document.id == document_id,
            Document.owner_id == current_user.id,
        )
        .first()
    )

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found.",
        )

    comment = Comment(
        document_id=document.id,
        user_id=current_user.id,
        guest_name=None,
        content=comment_data.content.strip(),
    )

    db.add(comment)
    db.commit()
    db.refresh(comment)

    return comment


# ============================================================
# GET AUTHENTICATED OWNER COMMENTS
# ============================================================

@router.get(
    "/{document_id}/comments",
    response_model=list[CommentResponse],
)
def get_comments(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    document = (
        db.query(Document)
        .filter(
            Document.id == document_id,
            Document.owner_id == current_user.id,
        )
        .first()
    )

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found.",
        )

    comments = (
        db.query(Comment)
        .filter(Comment.document_id == document.id)
        .order_by(Comment.created_at.asc())
        .all()
    )

    return comments


# ============================================================
# ADD GUEST COMMENT THROUGH SHARE LINK
# ============================================================

@router.post(
    "/shared/{token}/comments",
    response_model=CommentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_guest_comment(
    token: str,
    comment_data: GuestCommentCreate,
    db: Session = Depends(get_db),
):
    share = (
        db.query(Share)
        .filter(Share.token == token)
        .first()
    )

    if not share:
        raise HTTPException(
            status_code=404,
            detail="Invalid share link.",
        )

    document = (
        db.query(Document)
        .filter(Document.id == share.document_id)
        .first()
    )

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found.",
        )

    comment = Comment(
        document_id=document.id,
        user_id=None,
        guest_name=comment_data.guest_name.strip(),
        content=comment_data.content.strip(),
    )

    db.add(comment)
    db.commit()
    db.refresh(comment)

    return comment


# ============================================================
# GET GUEST COMMENTS THROUGH SHARE LINK
# ============================================================

@router.get(
    "/shared/{token}/comments",
    response_model=list[CommentResponse],
)
def get_guest_comments(
    token: str,
    db: Session = Depends(get_db),
):
    share = (
        db.query(Share)
        .filter(Share.token == token)
        .first()
    )

    if not share:
        raise HTTPException(
            status_code=404,
            detail="Invalid share link.",
        )

    comments = (
        db.query(Comment)
        .filter(Comment.document_id == share.document_id)
        .order_by(Comment.created_at.asc())
        .all()
    )

    return comments


# ============================================================
# GET SINGLE DOCUMENT
# ============================================================

@router.get(
    "/{document_id}",
    response_model=DocumentResponse,
)
def get_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    document = (
        db.query(Document)
        .filter(
            Document.id == document_id,
            Document.owner_id == current_user.id,
        )
        .first()
    )

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found.",
        )

    return document

@router.post(
    "/{document_id}/chat",
    response_model=ChatResponse,
)
def chat_with_document(
    document_id: int,
    chat_data: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    document = (
        db.query(Document)
        .filter(
            Document.id == document_id,
            Document.owner_id == current_user.id,
        )
        .first()
    )

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found.",
        )

    chat_service = ChatService()

    history = [
        {
            "role": message.role,
            "content": message.content,
        }
        for message in chat_data.history[-10:]
    ]

    answer, sources = chat_service.generate_answer(
        question=chat_data.question,
        document_id=document.id,
        history=history,
    )

    return ChatResponse(
        answer=answer,
        sources=sources,
    )

@router.post(
    "/shared/{token}/chat",
    response_model=ChatResponse,
)
def chat_with_shared_document(
    token: str,
    chat_data: ChatRequest,
    db: Session = Depends(get_db),
):
    share = (
        db.query(Share)
        .filter(Share.token == token)
        .first()
    )

    if not share:
        raise HTTPException(
            status_code=404,
            detail="Invalid share link.",
        )

    document = (
        db.query(Document)
        .filter(Document.id == share.document_id)
        .first()
    )

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found.",
        )

    chat_service = ChatService()

    history = [
        {
            "role": message.role,
            "content": message.content,
        }
        for message in chat_data.history[-10:]
    ]

    answer, sources = chat_service.generate_answer(
        question=chat_data.question,
        document_id=document.id,
        history=history,
    )

    return ChatResponse(
        answer=answer,
        sources=sources,
    )