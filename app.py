import streamlit as st
import requests

# ==========================================
# CONFIG
# ==========================================

BACKEND_URL = "http://localhost:8000/chat"  

st.set_page_config(
    page_title="A1B2C3 HR Support Chatbot",
    page_icon="🏢",
    layout="wide"
)

# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:
    st.title("🏢 HR Support Chatbot")
    st.markdown("""
Adaptive Hybrid RAG System

Features:
- Hybrid Retrieval (Dense + BM25)
- Cross Encoder Reranking
- Intent Routing
- Query Rewriting
- Evaluation Logging
    """)

    if st.button("🗑 Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# ==========================================
# MAIN TITLE
# ==========================================

st.title("🏢 A1B2C3 HR Support Chatbot")

# ==========================================
# SESSION STATE
# ==========================================

if "messages" not in st.session_state:
    st.session_state.messages = []

# ==========================================
# DISPLAY HISTORY
# ==========================================

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ==========================================
# CHAT INPUT
# ==========================================

if prompt := st.chat_input("Ask your HR-related question..."):

    # Show user message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.spinner("Thinking..."):

        try:
            response = requests.post(
                BACKEND_URL,
                json={"question": prompt},
                timeout=60
            )

            if response.status_code != 200:
                raise Exception(response.text)

            data = response.json()

            answer = data.get("answer", "")
            sources = data.get("sources", [])

        except Exception as e:
            answer = f"⚠️ Connection Error: {str(e)}"
            sources = []

    # Show assistant message
    with st.chat_message("assistant"):
        st.markdown(answer)

        if sources:
            st.markdown("### 📄 Policy Sources")

            for src in sources:
                policy = src.get("policy_name", "Policy")
                snippet = src.get("preview", "")

                with st.expander(policy):
                    st.write(snippet)

    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )