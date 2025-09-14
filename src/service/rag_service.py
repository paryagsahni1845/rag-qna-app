import os
from dotenv import load_dotenv
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_community.vectorstores import Chroma

# Local imports
from src.components.data_loader import load_and_chunk_pdf
from src.components.llm import get_llm, get_embeddings

# Load API keys from .env
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# HF_TOKEN is no longer needed here as it's loaded in llm.py
# HF_TOKEN = os.getenv("HF_TOKEN") 

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
        embeddings = get_embeddings() # Removed the HF_TOKEN argument
        Chroma.from_documents(documents, embeddings, persist_directory=CHROMA_DB_DIR)
        print("Vector store initialized and saved.")

def get_qa_chain():
    """
    Creates and returns a conversational retrieval chain.
    """
    if not os.path.exists(CHROMA_DB_DIR) or not os.listdir(CHROMA_DB_DIR):
        raise RuntimeError("Vector store not found. Run src/main.py first.")
    
    llm = get_llm() 
    embeddings = get_embeddings() 
    vector_store = Chroma(
        embedding_function=embeddings,
        persist_directory=CHROMA_DB_DIR
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