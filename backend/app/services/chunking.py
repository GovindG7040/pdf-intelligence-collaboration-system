from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


class DocumentChunker:
    """
    Splits loaded documents into smaller chunks
    for embedding and retrieval.
    """

    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 100,):

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

    # ======================================================
    # SPLIT DOCUMENTS
    # ======================================================

    def split_documents(self, documents: list[Document],) -> list[Document]:

        chunks = self.text_splitter.split_documents(
            documents
        )

        

        return chunks