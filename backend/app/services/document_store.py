from pathlib import Path

from langchain_chroma import Chroma

from app.services.embedding_service import EmbeddingService


class DocumentStore:

    def __init__(self):
        project_root = Path(__file__).resolve().parents[3]

        chroma_path = project_root / "chroma_db"

        embedding_service = EmbeddingService()

        self.vector_store = Chroma(
            persist_directory=str(chroma_path),
            embedding_function=(
                embedding_service.get_embedding_model()
            ),
        )

    def add_documents(self, documents):
        self.vector_store.add_documents(documents)

    def get_vector_store(self):
        return self.vector_store