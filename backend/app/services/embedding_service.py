from langchain_core.embeddings import Embeddings
from google import genai
from google.genai import types

from app.core.config import settings


class EmbeddingService(Embeddings):
    """
    Uses Gemini Embeddings API instead of loading a local
    HuggingFace/SentenceTransformer model.

    This significantly reduces server memory usage.
    """

    def __init__(self):
        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )

        self.model_name = "gemini-embedding-001"
        self.output_dimensionality = 768

        print("Gemini embedding service initialized.")

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """
        Generate embeddings for document chunks.
        """

        if not texts:
            return []

        result = self.client.models.embed_content(
            model=self.model_name,
            contents=texts,
            config=types.EmbedContentConfig(
                task_type="RETRIEVAL_DOCUMENT",
                output_dimensionality=self.output_dimensionality,
            ),
        )

        return [
            embedding.values
            for embedding in result.embeddings
        ]

    def embed_query(self, text: str) -> list[float]:
        """
        Generate an embedding for a user search query.
        """

        result = self.client.models.embed_content(
            model=self.model_name,
            contents=text,
            config=types.EmbedContentConfig(
                task_type="RETRIEVAL_QUERY",
                output_dimensionality=self.output_dimensionality,
            ),
        )

        return result.embeddings[0].values

    def get_embedding_model(self):
        """
        Kept for compatibility with the existing DocumentStore.
        """

        return self