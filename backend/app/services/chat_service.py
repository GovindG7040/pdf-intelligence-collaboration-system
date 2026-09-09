from typing import Any

from app.services.bm25_instance import bm25_service
from app.services.document_store import DocumentStore
from app.services.gemini_service import GeminiService
from app.services.reranker_service import RerankerService


class ChatService:
    """
    Handles document-scoped RAG chat.

    Pipeline:
        1. Rewrite follow-up question
        2. Retrieve relevant chunks from Chroma
        3. Retrieve keyword matches from BM25 when available
        4. Merge and deduplicate results
        5. Rerank using CrossEncoder
        6. Generate answer using Gemini
    """

    def __init__(self):
        print("Initializing Chat Service...")

        # Uses the same Chroma database created during PDF upload.
        self.document_store = DocumentStore()
        self.vector_store = self.document_store.get_vector_store()

        self.reranker = RerankerService()
        self.gemini = GeminiService()

        print("Chat Service initialized.")

    # =====================================================
    # QUERY REWRITING
    # =====================================================

    def rewrite_query(
        self,
        question: str,
        history: list[dict[str, str]],
    ) -> str:
        """
        Converts a follow-up question into a standalone search query.
        """

        if not history:
            return question.strip()

        recent_history = history[-6:]

        history_text = "\n".join(
            f"{message.get('role', 'user').upper()}: "
            f"{message.get('content', '')}"
            for message in recent_history
        )

        prompt = f"""
You rewrite questions for document retrieval.

Conversation history:
{history_text}

Current question:
{question}

Rewrite the current question as a standalone search query.

Rules:
- Preserve the user's original meaning.
- Resolve references such as "it", "this", "that", "they", etc.
- Include important context from the conversation when necessary.
- Do not answer the question.
- Return ONLY the rewritten search query.
"""

        try:
            rewritten = self.gemini.generate_text(prompt)

            if rewritten:
                return rewritten.strip()

        except Exception:
            # If rewriting fails, continue with the original question.
            pass

        return question.strip()

    # =====================================================
    # DOCUMENT RETRIEVAL
    # =====================================================

    def retrieve_documents(
        self,
        query: str,
        document_id: int,
        k: int = 20,
    ) -> list[Any]:

        retrieved_documents = []

        # -------------------------------------------------
        # CHROMA / DENSE RETRIEVAL
        # -------------------------------------------------

        try:
            dense_documents = self.vector_store.similarity_search(
                query,
                k=k,
                filter={
                    "document_id": str(document_id)
                },
            )

            retrieved_documents.extend(dense_documents)

        except Exception as exc:
            print(f"Chroma retrieval failed: {exc}")

        # -------------------------------------------------
        # BM25 / KEYWORD RETRIEVAL
        # -------------------------------------------------

        try:
            bm25_documents = bm25_service.retrieve(
                query=query,
                k=k,
            )

            # BM25 is currently global, so explicitly restrict
            # results to the requested document.
            bm25_documents = [
                document
                for document in bm25_documents
                if str(document.metadata.get("document_id"))
                == str(document_id)
            ]

            retrieved_documents.extend(bm25_documents)

        except Exception as exc:
            # BM25 may not have been built yet.
            # Dense retrieval can still handle the request.
            print(f"BM25 retrieval skipped: {exc}")

        # -------------------------------------------------
        # DEDUPLICATION
        # -------------------------------------------------

        unique_documents = []
        seen = set()

        for document in retrieved_documents:

            content = document.page_content.strip()

            if not content:
                continue

            key = (
                str(document.metadata.get("document_id")),
                str(document.metadata.get("page")),
                content,
            )

            if key in seen:
                continue

            seen.add(key)
            unique_documents.append(document)

        return unique_documents

    # =====================================================
    # CONTEXT BUILDING
    # =====================================================

    def build_context(
        self,
        documents: list[Any],
    ) -> str:

        context_parts = []

        for index, document in enumerate(documents, start=1):

            page = document.metadata.get("page", "unknown")

            context_parts.append(
                f"""
SOURCE {index}
PAGE: {page}

{document.page_content}
""".strip()
            )

        return "\n\n---\n\n".join(context_parts)

    # =====================================================
    # ANSWER GENERATION
    # =====================================================

    def generate_answer(
        self,
        question: str,
        document_id: int,
        history: list[dict[str, str]] | None = None,
    ) -> tuple[str, list[int]]:

        history = history or []

        # -------------------------------------------------
        # 1. REWRITE FOLLOW-UP QUESTION
        # -------------------------------------------------

        retrieval_query = self.rewrite_query(
            question=question,
            history=history,
        )

        print(f"Original question: {question}")
        print(f"Retrieval query: {retrieval_query}")

        # -------------------------------------------------
        # 2. RETRIEVE
        # -------------------------------------------------

        retrieved_documents = self.retrieve_documents(
            query=retrieval_query,
            document_id=document_id,
            k=20,
        )

        if not retrieved_documents:
            return (
                "I could not find relevant information in this PDF "
                "to answer your question.",
                [],
            )

        # -------------------------------------------------
        # 3. RERANK
        # -------------------------------------------------

        reranked_documents = self.reranker.rerank(
            question=retrieval_query,
            documents=retrieved_documents,
            top_k=5,
        )

        # -------------------------------------------------
        # 4. BUILD CONTEXT
        # -------------------------------------------------

        context = self.build_context(reranked_documents)

        # -------------------------------------------------
        # 5. GENERATE ANSWER
        # -------------------------------------------------

        history_text = ""

        if history:
            recent_history = history[-6:]

            history_text = "\n".join(
                f"{message.get('role', 'user').upper()}: "
                f"{message.get('content', '')}"
                for message in recent_history
            )

        prompt = f"""
You are an AI assistant answering questions about a PDF document.

Use ONLY the information contained in the provided PDF context.

If the answer cannot be found in the context, clearly say that
the information is not available in the PDF.

Do not invent facts.
Do not use outside knowledge.
Keep the answer clear and concise.

Conversation history:
{history_text}

PDF CONTEXT:
{context}

CURRENT QUESTION:
{question}

Answer the question using the PDF context.
"""

        answer = self.gemini.generate_text(prompt)

        # -------------------------------------------------
        # 6. RETURN SOURCE PAGES
        # -------------------------------------------------

        sources = []

        for document in reranked_documents:

            page = document.metadata.get("page")

            if page is not None:
                try:
                    page_number = int(page)

                    if page_number not in sources:
                        sources.append(page_number)

                except (TypeError, ValueError):
                    pass

        return answer.strip(), sources

    # =====================================================
    # BACKWARD-COMPATIBLE ASK METHOD
    # =====================================================

    def ask(
        self,
        question: str,
        document_id: int,
        history: list[dict[str, str]] | None = None,
    ) -> dict:

        answer, sources = self.generate_answer(
            question=question,
            document_id=document_id,
            history=history,
        )

        return {
            "answer": answer,
            "sources": sources,
        }