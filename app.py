import streamlit as st
import os
from src.chatbot.agent import create_product_agent

# Set OpenMP fix for macOS
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

st.set_page_config(page_title="Vector Pricer", page_icon="💻", layout="wide")
st.title("Vector Pricer")
st.markdown("Ask a question about Macbook Air or Macbook Pro laptops or type 'quit' to exit")

st.sidebar.header("Vector Pricer Quick Questions: ")
samples = [
    "What is the price of the Macbook Air with M2 chip?",
    "What is the price of the Macbook Pro with M2 chip?",
]

for sample in samples:
    if st.sidebar.button(sample):
        st.session_state.query = sample

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display history 
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# User input
if prompt := st.chat_input("Ask a question about Macbook Air or Macbook Pro laptops or type 'quit' to exit"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("Agent is Thinking..."):
            agent = create_product_agent()
            result = agent.invoke({"input": prompt})
            response = result.get("output") if isinstance(result, dict) else result
            st.markdown(response)
            
    st.session_state.messages.append({"role": "assistant", "content": response})

# Clear
if st.sidebar.button("Clear"):
    st.session_state.messages = []
    st.rerun()