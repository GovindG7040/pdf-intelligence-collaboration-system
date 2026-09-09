from datetime import datetime

from pydantic import BaseModel, Field


class DocumentResponse(BaseModel):
    id: int
    filename: str
    summary: str | None
    created_at: datetime

    class Config:
        from_attributes = True


class ShareResponse(BaseModel):
    token: str
    invited_email: str | None
    share_url: str


class CommentCreate(BaseModel):
    content: str = Field(..., min_length=1, max_length=2000)


class GuestCommentCreate(BaseModel):
    guest_name: str = Field(..., min_length=1, max_length=100)
    content: str = Field(..., min_length=1, max_length=2000)


class CommentResponse(BaseModel):
    id: int
    document_id: int
    user_id: int | None
    guest_name: str | None
    content: str
    created_at: datetime

    class Config:
        from_attributes = True