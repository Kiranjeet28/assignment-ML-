import os
import base64

import requests
import pandas as pd
import streamlit as st

API_URL = "http://localhost:8000/ask"

# Resolve dataset path relative to this file
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "titanic.csv")

st.set_page_config(page_title="Titanic Chat Agent", layout="wide")
st.title("🚢 Titanic Dataset Chat Agent")
st.caption("Powered by Qwen2.5-7B-Instruct via Together AI")


# ── Sidebar: dataset summary ──────────────────────────────────────────────────
def show_sidebar():
    st.sidebar.header("📊 Dataset Summary")
    try:
        df = pd.read_csv(DATA_PATH)
        st.sidebar.metric("Rows", df.shape[0])
        st.sidebar.metric("Columns", df.shape[1])
        st.sidebar.markdown("**Columns:**")
        st.sidebar.write(list(df.columns))
        with st.sidebar.expander("Preview (first 5 rows)"):
            st.dataframe(df.head())
    except Exception:
        st.sidebar.error("Could not load Titanic dataset. Run setup_project.py first.")


show_sidebar()

# ── Chat history ──────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state["messages"] = []

for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("plot_base64"):
            st.image(
                base64.b64decode(msg["plot_base64"]),
                use_container_width=True,
            )

# ── User input ────────────────────────────────────────────────────────────────
user_input = st.chat_input("Ask anything about the Titanic dataset...")

if user_input:
    # Show user message immediately
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state["messages"].append({"role": "user", "content": user_input})

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                resp = requests.post(
                    API_URL,
                    json={"question": user_input},
                    timeout=60,         # Qwen2.5 via Together AI can be slow on first call
                )
                resp.raise_for_status()
                data = resp.json()

                st.markdown(data["text_answer"])

                plot_b64 = data.get("plot_base64")
                if data.get("plot_needed") and plot_b64:
                    st.image(base64.b64decode(plot_b64), use_container_width=True)

                assistant_msg: dict = {"role": "assistant", "content": data["text_answer"]}
                if plot_b64:
                    assistant_msg["plot_base64"] = plot_b64
                st.session_state["messages"].append(assistant_msg)

            except requests.exceptions.ConnectionError:
                st.error("Cannot reach the backend. Make sure uvicorn is running on port 8000.")
            except Exception as e:
                st.error(f"Error: {e}")

    # Use st.rerun() — st.experimental_rerun() was removed in Streamlit ≥ 1.27
    st.rerun()