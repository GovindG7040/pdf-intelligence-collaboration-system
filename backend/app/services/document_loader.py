from pathlib import Path

from langchain_core.documents import Document

from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
)

# ==========================================================
# SUPPORTED FILE TYPES
# ==========================================================

SUPPORTED_EXTENSIONS = {
    ".md",
    ".txt",
    ".pdf",
}


class DocumentLoader:
    """
    Loads supported documents from a directory.

    Supported formats:
        - Markdown (.md)
        - Text (.txt)
        - PDF (.pdf)

    Returns:
        List[Document]
    """

    def __init__(self, folder_path: str):

        self.folder_path = Path(folder_path)

    # ======================================================
    # LOAD DOCUMENTS
    # ======================================================

    def load_documents(self) -> list[Document]:

        documents = []

        if not self.folder_path.exists():
            raise FileNotFoundError(f"Folder not found: {self.folder_path}" )

        # Search all files recursively

        for file_path in self.folder_path.rglob("*"):

            if not file_path.is_file():
                continue

            extension = file_path.suffix.lower()

            if extension not in SUPPORTED_EXTENSIONS:
                continue

            print(f"Loading: {file_path.name}")

            if extension in [".md", ".txt"]:

                loader = TextLoader(str(file_path), encoding="utf-8")

            elif extension == ".pdf":

                loader = PyPDFLoader(str(file_path))

            else:
                continue

            docs = loader.load()

            # --------------------------------------------------
            # Add metadata
            # --------------------------------------------------

            for doc in docs:

                doc.metadata["file_name"] = file_path.name
                doc.metadata["extension"] = extension

            documents.extend(docs)

       

        return documents