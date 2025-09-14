import os
import re # Import the regular expression module
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document

def clean_text_for_encoding(text: str) -> str:
    """
    Cleans text to remove problematic Unicode characters that can cause encoding errors.
    """
    # Remove surrogate characters
    cleaned_text = re.sub(r'[\ud800-\udfff]', '', text)
    # Optional: Replace non-ASCII characters with a placeholder or remove them
    # This is a more aggressive cleanup, useful if the problem persists
    # cleaned_text = cleaned_text.encode('ascii', 'ignore').decode('ascii')
    return cleaned_text

def load_and_chunk_pdf(file_path: str, chunk_size: int = 1000, chunk_overlap: int = 200):
    """
    Loads a PDF document, cleans the text, and splits it into text chunks.

    Args:
        file_path: Path to the PDF document.
        chunk_size: The size of each text chunk.
        chunk_overlap: The overlap between consecutive chunks.

    Returns:
        A list of LangChain Document objects.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The PDF file was not found at: {file_path}")

    print(f"Loading document from {file_path}...")
    loader = PyPDFLoader(file_path)
    documents = loader.load()

    # Clean the page content of each document before splitting
    cleaned_documents = []
    for doc in documents:
        cleaned_content = clean_text_for_encoding(doc.page_content)
        cleaned_documents.append(Document(page_content=cleaned_content, metadata=doc.metadata))

    print("Splitting document into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len
    )
    return text_splitter.split_documents(cleaned_documents)
