import os
from dotenv import load_dotenv

load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
hf_token = os.getenv("HF_TOKEN")

from langchain_huggingface import HuggingFaceEmbeddings
embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-large-en-v1.5",  # small, fast, good for RAG
    model_kwargs={"token": hf_token}
)

from langchain_groq import ChatGroq

llm = ChatGroq(
    groq_api_key=groq_api_key,
    model_name="llama-3.1-8b-instant"  # updated
)


def get_llm():
    """Return Groq-powered LLM."""
    return llm

def get_embeddings():
    """Return HuggingFace embeddings model."""
    return embeddings
