from langchain_huggingface import HuggingFaceEmbeddings


class EmbeddingService:
    """
    Loads and provides the embedding model
    used throughout the application.
    """

    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2",):

        self.embedding_model = HuggingFaceEmbeddings(
            model_name=model_name
        )

        print("Embedding model loaded successfully.")

    # ======================================================
    # RETURN EMBEDDING MODEL
    # ======================================================

    def get_embedding_model(self):

        return self.embedding_model