from langchain_community.retrievers import BM25Retriever

from langchain_core.documents import Document


class BM25Service:
    """
    Builds and manages the BM25 keyword retriever.
    """

    def __init__(self):

        self.retriever = None

        print("BM25 Service initialized.")

    # =====================================================
    # BUILD INDEX
    # =====================================================

    def build_index(self, documents: list[Document],):
        """
        Builds the BM25 index from documents.
        """

        self.retriever = BM25Retriever.from_documents(
            documents
        )

        print(
            f"BM25 index built with {len(documents)} documents."
        )

    # =====================================================
    # RETRIEVE DOCUMENTS
    # =====================================================

    def retrieve(self, query: str, k: int = 10,):
        """
        Retrieves relevant documents using BM25.
        """

        if self.retriever is None:

            raise ValueError("BM25 index has not been built.")

        self.retriever.k = k

        return self.retriever.invoke(query)