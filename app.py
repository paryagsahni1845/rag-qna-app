import sys
import pysqlite3
sys.modules["sqlite3"] = pysqlite3
import streamlit as st
from langchain_core.messages import HumanMessage
from src.service.rag_service import get_qa_chain

# Streamlit UI and Logic 
st.set_page_config(page_title="RAG-QnA Chatbot", layout="centered")
st.title("📘 RAG-QnA Chatbot")
st.markdown(
    """
    Ask me anything about **machine learning** — I’ll answer using content directly from  
    *Hands-On Machine Learning with Scikit-Learn and TensorFlow*.  
    """
)

# Initialize the RAG chain and chat history
if "qa_chain" not in st.session_state:
    try:
        st.session_state.qa_chain = get_qa_chain()
    except RuntimeError as e:
        st.error(str(e))
        st.stop()
        
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display chat messages
for message in st.session_state.chat_history:
    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.markdown(message.content)
    else:
        with st.chat_message("assistant"):
            st.markdown(message.content)

# Handle user input
if user_query := st.chat_input("Ask a question..."):
    with st.chat_message("user"):
        st.markdown(user_query)

    # Run the RAG pipeline with user query
    with st.spinner("Thinking..."):
        try:
            response = st.session_state.qa_chain.invoke(
                {"question": user_query, "chat_history": st.session_state.chat_history}
            )
            ai_response = response["answer"]
            st.session_state.chat_history.append(HumanMessage(content=user_query))
            st.session_state.chat_history.append(response["chat_history"][-1])

        except Exception as e:
            ai_response = f"An error occurred: {e}"
            st.error(ai_response)

    with st.chat_message("assistant"):
        st.markdown(ai_response)
        
    # Display source documents
    if "source_documents" in response and response["source_documents"]:
        with st.expander("Show Sources"):
            for i, doc in enumerate(response["source_documents"]):
                st.write(f"**Source {i+1}**")
                st.write(f"Page: {doc.metadata.get('page')}")
                st.code(doc.page_content, language='markdown')
