from pathlib import Path

from pypdf import PdfReader
from langchain_core.documents import Document as LangChainDocument
from langchain_text_splitters import RecursiveCharacterTextSplitter


class PDFService:

    MAX_FILE_SIZE = 20 * 1024 * 1024  # 20 MB

    def validate_pdf(self, file_path: Path) -> PdfReader:
        if not file_path.exists():
            raise ValueError("Uploaded file does not exist.")

        if file_path.stat().st_size > self.MAX_FILE_SIZE:
            raise ValueError("PDF file is too large. Maximum size is 20 MB.")

        with open(file_path, "rb") as file:
            header = file.read(5)

        if header != b"%PDF-":
            raise ValueError("Invalid PDF file.")

        try:
            reader = PdfReader(str(file_path))
        except Exception as exc:
            raise ValueError("Unable to read the PDF file.") from exc

        if len(reader.pages) == 0:
            raise ValueError("PDF contains no pages.")

        return reader

    def extract_documents(
        self,
        reader: PdfReader,
        document_id: int,
        owner_id: int,
        filename: str,
    ):
        documents = []

        for page_number, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""

            if not text.strip():
                continue

            documents.append(
                LangChainDocument(
                    page_content=text,
                    metadata={
                        "document_id": str(document_id),
                        "owner_id": str(owner_id),
                        "file_name": filename,
                        "page": page_number,
                    },
                )
            )

        if not documents:
            raise ValueError(
                "Could not extract readable text from this PDF."
            )

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=150,
        )

        return splitter.split_documents(documents)

    def extract_full_text(self, reader: PdfReader) -> str:
        pages = []

        for page in reader.pages:
            text = page.extract_text() or ""

            if text.strip():
                pages.append(text)

        return "\n\n".join(pages)