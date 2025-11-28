"""
Vector database setup and operations using Chroma.

This manages document storage and semantic search.
"""

from typing import List, Dict
from datetime import datetime
import logging

import chromadb
from chromadb.utils import embedding_functions
from config.settings import OPENAI_API_KEY, BASE_DIR

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


chroma_client = chromadb.PersistentClient(path=str(BASE_DIR / "chroma_db"))

openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=OPENAI_API_KEY,
    model_name="text-embedding-3-small"
)

collection = chroma_client.get_or_create_collection(
    name="document_chunks",
    embedding_function=openai_ef
)


async def store_document_chunks(
    document_id: str,
    chunks: List[str],
    source: str = None
) -> Dict[str, any]:
    """
    Store document chunks in vector database with metadata.
    
    Args:
        document_id: Unique identifier for the document
        chunks: List of text chunks to store
        source: Source filename (e.g., "machine_learning.pdf")
        
    Returns:
        {
            "status": "success" | "failed",
            "chunks_stored": int,
            "error": str (only if failed)
        }
        
    What Happens Automatically:
        - Chroma creates embeddings for each chunk using OpenAI
        - Embeddings are vector representations of text meaning
        - These enable semantic search later
        
    Resources:
        - Chroma docs: https://docs.trychroma.com/
        - What are embeddings?: https://platform.openai.com/docs/guides/embeddings
    """
    if not chunks:
        logger.warning(f"No chunks to store for document {document_id}")
        return {"status": "success", "chunks_stored": 0}
    
    try:
        timestamp = datetime.utcnow().isoformat() + "Z"
        
        ids = [f"{document_id}_chunk_{i}" for i in range(len(chunks))]
        
        metadatas = [
            {
                "document_id": document_id,
                "chunk_index": i,
                "source": source or "unknown",
                "timestamp": timestamp
            }
            for i in range(len(chunks))
        ]
        
        collection.add(
            documents=chunks,
            ids=ids,
            metadatas=metadatas
        )
        
        logger.info(f"Successfully stored {len(chunks)} chunks for document {document_id} (source: {source})")
        
        return {
            "status": "success",
            "chunks_stored": len(chunks)
        }
        
    except Exception as e:
        error_msg = f"Failed to store chunks for document {document_id}: {str(e)}"
        logger.error(error_msg)
        return {
            "status": "failed",
            "chunks_stored": 0,
            "error": str(e)
        }


async def search_documents(query: str, document_ids: List[str] = None, n_results: int = 5) -> Dict:
    """
    Search for relevant document chunks using semantic similarity.
    
    Args:
        query: Search query (question or topic)
        document_ids: Optional list of document IDs to search within
        n_results: Number of results to return
        
    Returns:
        {
            "chunks": ["text chunk 1", "text chunk 2", ...],
            "ids": ["doc_123_chunk_5", ...],
            "metadatas": [{"document_id": "doc_123", "chunk_index": 5}, ...]
        }
        
    How Semantic Search Works:
        1. Your query gets converted to an embedding (vector)
        2. Chroma finds chunks with similar embeddings
        3. Similar embeddings = similar meaning
        4. This finds relevant info even if words don't match exactly
        
    Example:
        Query: "What role did France play?"
        Might find: "French military support was crucial..." 
        Even though "France" and "French" are different words!
    """
    where_filter = None
    if document_ids:
        where_filter = {"document_id": {"$in": document_ids}}
    
    results = collection.query(
        query_texts=[query],
        n_results=n_results,
        where=where_filter
    )
    
    return {
        "chunks": results['documents'][0] if results['documents'] else [],
        "ids": results['ids'][0] if results['ids'] else [],
        "metadatas": results['metadatas'][0] if results['metadatas'] else []
    }


async def get_all_chunks_for_documents(document_ids: List[str]) -> List[str]:
    """
    Retrieve all chunks for specific documents.
    
    Args:
        document_ids: List of document IDs
        
    Returns:
        List of all text chunks from those documents
        
    Use Case:
        When generating podcasts, you might want ALL content
        from selected documents, not just relevant chunks.
    """
    if not document_ids:
        return []
    
    results = collection.get(
        where={"document_id": {"$in": document_ids}}
    )
    
    return results['documents'] if results['documents'] else []