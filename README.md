# RAG-QnA Chatbot for "Hands-On Machine Learning"

## Project Overview
This project is a modular, production-ready **RAG (Retrieval-Augmented Generation)** chatbot designed to answer questions from the book, *Hands-On Machine Learning with Scikit-Learn and TensorFlow*. The system uses a local-first approach with open-source components, is fully containerized with Docker, and can be deployed on platforms like Streamlit Cloud.

The core of this system is its ability to provide detailed, contextual answers sourced directly from the book, complete with page number citations.

## Core Objectives
- **Develop a Modular Pipeline**: Architect a clean, maintainable RAG pipeline with separate components for data loading, embedding, and model serving.
- **Ensure Reproducibility**: Containerize the entire application using Docker to guarantee a consistent environment across development and deployment.
- **Enable Scalable Deployment**: The system is designed for easy deployment on cloud platforms like Streamlit Cloud, leveraging its native secrets management for security.
- **Create an Intuitive Interface**: Provide a user-friendly chat interface with Streamlit, allowing for seamless conversation and clear display of source documents.
- **Utilize Open-Source Models**: Employ powerful open-source models for embeddings and language generation to create a robust and cost-effective solution.

## Project Structure
The project follows a modular and well-organized directory structure to separate concerns and ensure maintainability.

```text
RAG/
├── artifacts/
│   └── chroma_db/       # Persistent vector store and model artifacts
├── src/
│   ├── components/
│   │   ├── data_loader.py  # Handles PDF loading and text chunking
│   │   ├── llm.py          # Manages LLM and embedding models
│   │   └── __init__.py
│   ├── service/
│   │   ├── rag_service.py  # The core RAG pipeline logic
│   │   └── __init__.py
│   └── main.py             # Script to initialize the vector store
├── Dockerfile              # Docker configuration for building the app image
├── .gitignore              # Files and folders to ignore for version control
├── app.py                  # Main Streamlit application file
├── mlbook.pdf              # The source document for the RAG pipeline
└── requirements.txt        # List of all Python dependencies
```
## Methodology

### 1. Data Ingestion & Indexing
The book, `mlbook.pdf`, serves as the knowledge base. The document is loaded and split into manageable text chunks. These chunks are transformed into numerical vector embeddings using the **BAAI/bge-large-en-v1.5** model from Hugging Face. The resulting vector store is persisted in **ChromaDB**, ensuring fast and efficient retrieval of relevant information.

### 2. Pipeline Architecture
The RAG pipeline is built using **LangChain**. It intelligently retrieves relevant text chunks from the ChromaDB vector store based on a user's query and previous conversation history. This contextual information is then passed to a large language model to formulate a coherent and accurate answer.

### 3. Model & Dependencies
- **Embedding Model**: BAAI/bge-large-en-v1.5 (via sentence-transformers)
- **Language Model**: llama3-8b (via Groq)
- **Vector Store**: ChromaDB

### 4. Deployment
The application is deployed on **Streamlit Cloud**, leveraging a Docker container to manage all dependencies and artifacts. This setup ensures that the environment is consistent and that the pre-built vector store is readily available, eliminating the need for time-consuming re-indexing on every deployment.

## User Interface and Experience

<img width="1313" height="534" alt="image" src="https://github.com/user-attachments/assets/ea973b2a-16c7-4cea-810b-a5fbc2768eb8" />

The web application's front-end is crafted with a clear and intuitive design using **Streamlit**. It provides a seamless chat experience with real-time feedback.

### Key Features:
- **Chat Interface**: A modern chat UI for natural language interaction.
- **Live Prediction**: User queries trigger the RAG pipeline, and the response is displayed with a "Thinking..." spinner.
- **Source Documents**: An expandable section reveals the specific text chunks and page numbers from the book used to generate the answer.

## System Architecture

### Application Architecture
- **Frontend**: Streamlit interactive chat interface
- **Backend**: Python RAG pipeline built with LangChain
- **Model**: LLM running on Groq's API
- **Vector Store**: ChromaDB persistent client

### Deployment Architecture
- **Container**: Docker image with a Python base
- **Hosting**: Streamlit Community Cloud
- **Secrets**: Streamlit Cloud Secrets Management for API keys

## Project Links
- **Live Demo**: [Streamlit app](https://rag-qna-app.streamlit.app/)
- **GitHub Repository**: [paryagsahni1845/rag-qna-app](https://github.com/paryagsahni1845/rag-qna-app)
