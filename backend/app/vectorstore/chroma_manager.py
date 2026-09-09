from langchain_chroma import Chroma

from app.services.embedding_service import EmbeddingService


class ChromaManager:
    """
    Creates and manages the Chroma vector database.
    """

    def __init__(self, persist_directory: str = "chroma_db",):

        self.embedding_service = EmbeddingService()

        self.embedding_model = (
            self.embedding_service.get_embedding_model()
        )

        self.vector_store = Chroma(
            persist_directory=persist_directory,
            embedding_function=self.embedding_model,
        )

        print("Chroma Vector Store Ready.")

    # =====================================================
    # CLEAR EXISTING COLLECTION
    # =====================================================

    def clear_collection(self):

        print("Clearing existing Chroma collection...")

        self.vector_store.reset_collection()

        print("Collection cleared.")


    # =====================================================
    # ADD DOCUMENTS
    # =====================================================

    def add_documents(self, documents):

        self.vector_store.add_documents(documents)

        print(f"Stored {len(documents)} chunks.")

    # =====================================================
    # RETURN VECTOR STORE
    # =====================================================

    def get_vector_store(self):

        return self.vector_store