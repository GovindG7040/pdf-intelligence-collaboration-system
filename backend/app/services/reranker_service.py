from sentence_transformers import CrossEncoder


class RerankerService:
    """
    Reranks retrieved documents using a CrossEncoder model.
    """

    def __init__(self, model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2",):

        print("Loading reranker model...")

        self.model = CrossEncoder(model_name)

        print("Reranker model loaded successfully.")

    # =====================================================
    # RERANK DOCUMENTS
    # =====================================================

    def rerank(self,
        question: str,
        documents: list,
        top_k: int = 5,
    ):
        """
        Returns the top_k most relevant documents.
        """

        if not documents:

            return []

        # ------------------------------------------
        # Create Question-Document Pairs
        # ------------------------------------------

        sentence_pairs = [(question, document.page_content) for document in documents]   # List of tuples (question, document content).list comprehension is used to create a list of tuples, where each tuple contains the question and the content of a document. This is done for all documents in the input list.

        # ------------------------------------------
        # Predict Relevance Scores
        # ------------------------------------------

        scores = self.model.predict(sentence_pairs)

        print("\n========== RERANKER ==========")

        print(f"Retrieved Documents : {len(documents)}")

        # ------------------------------------------
        # Combine Scores with Documents
        # ------------------------------------------

        scored_documents = list(zip(documents,scores,))        # List of tuples (document, score). The zip function is used to combine the list of documents and the list of scores into a single list of tuples, where each tuple contains a document and its corresponding relevance score.example: [(doc1, score1), (doc2, score2), ...]. if documents = [doc1, doc2, doc3] and scores = [score1, score2, score3], then scored_documents will be [(doc1, score1), (doc2, score2), (doc3, score3)].

        # ------------------------------------------
        # Sort by Score (Descending)
        # ------------------------------------------

        scored_documents.sort(key=lambda item: item[1], reverse=True,)  # Sorts the list of tuples based on the second element (score) in descending order. The lambda function is used to extract the score from each tuple for comparison. After sorting, the documents with the highest relevance scores will be at the beginning of the list.

        print("\nTop Ranked Documents:")

        for rank, (document, score) in enumerate(scored_documents[:top_k], start=1):

            print(f"{rank}. {document.metadata.get('source')}")

            print(f"   Score : {score:.4f}")

        # ------------------------------------------
        # Return Top Documents
        # ------------------------------------------

        reranked_documents = [document for document, score in scored_documents[:top_k]]

        return reranked_documents