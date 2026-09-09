from app.services.document_loader import DocumentLoader
from app.services.chunking import DocumentChunker
from app.vectorstore.chroma_manager import ChromaManager
from app.services.bm25_instance import bm25_service

class IngestService:
    """
    Coordinates the complete document ingestion pipeline.

    Workflow:
        Load Documents
            ↓
        Split into Chunks
            ↓
        Store in ChromaDB
    """

    def __init__(self, knowledge_base_path: str = "../knowledge_base",):

        self.loader = DocumentLoader(knowledge_base_path)

        self.chunker = DocumentChunker()

        self.chroma_manager = ChromaManager()

    # =====================================================
    # INGEST DOCUMENTS
    # =====================================================

    def ingest(self):

        print("\n========== INGESTION STARTED ==========\n")

        # -----------------------------
        # STEP 1: Load & Chunk Documents
        # -----------------------------

        chunks = self.load_chunks()

        print(f"Created {len(chunks)} chunks.\n")

        # -----------------------------
        # STEP 2: Clear Existing Chroma Collection
        # -----------------------------

        self.chroma_manager.clear_collection()

        # -----------------------------
        # STEP 3: Store Chunks in ChromaDB
        # -----------------------------

        self.chroma_manager.add_documents(chunks)

        # -----------------------------
        # STEP 4: Rebuild BM25 Index
        # -----------------------------

        print("\nRebuilding BM25 Index...")

        bm25_service.build_index(chunks)

        print("BM25 Index Updated.")

        print("\n========== INGESTION COMPLETED ==========\n")
        
        # =====================================================
        # LOAD CHUNKS
        # =====================================================

    def load_chunks(self):
        """
        Loads and chunks the knowledge base without storing it.
        Used for building the BM25 index.
        """

        documents = self.loader.load_documents()

        chunks = self.chunker.split_documents(
            documents
        )

        return chunks    