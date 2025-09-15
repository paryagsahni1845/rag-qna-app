import os
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_community.vectorstores import Chroma
import chromadb
from chromadb.config import Settings # 🔹 Import Settings for ChromaDB configuration

# Local imports
from src.components.data_loader import load_and_chunk_pdf
from src.components.llm import get_embeddings, get_llm

# Configuration constants
PDF_FILE_PATH = "mlbook.pdf"
CHROMA_DB_DIR = "artifacts/chroma_db"

def initialize_vector_store():
    """
    Initializes or loads the ChromaDB vector store.
    This function should be called once, e.g., via the main.py script.
    """
    if os.path.exists(CHROMA_DB_DIR) and os.listdir(CHROMA_DB_DIR):
        print("Vector store already exists. Skipping initialization.")
    else:
        print("Initializing vector store for the first time...")
        documents = load_and_chunk_pdf(PDF_FILE_PATH)
        embeddings = get_embeddings()
        
        # Corrected: Use a persistent client with explicit settings
        client = chromadb.PersistentClient(path=CHROMA_DB_DIR)
        
        Chroma.from_documents(documents, embeddings, client=client)
        print("Vector store initialized and saved.")

def get_qa_chain():
    """
    Creates and returns a conversational retrieval chain.
    """
    if not os.path.exists(CHROMA_DB_DIR) or not os.listdir(CHROMA_DB_DIR):
        raise RuntimeError("Vector store not found. Run src/main.py first.")
    
    llm = get_llm()
    embeddings = get_embeddings()
    
    # Corrected: Use a persistent client with explicit settings
    client = chromadb.PersistentClient(path=CHROMA_DB_DIR)
    
    vector_store = Chroma(
        embedding_function=embeddings,
        client=client
    )
    
    retriever = vector_store.as_retriever(search_kwargs={"k": 5})

    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        output_key="answer"
    )

    return ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        return_source_documents=True,
        chain_type="stuff"
    )
