import base64
import os

import streamlit as st
from dotenv import load_dotenv
from together import Together

load_dotenv()

api_key = st.secrets["Together"]["TOGETHER_API_KEY"]

client = Together(api_key=api_key)

col1, col2 = st.columns([1, 5])

with col1:
    st.image("Kakgem.png", width=100)
with col2:
    st.header("Mari Tanya :blue[Kak Gem]", divider="blue")



if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "Saya adalah kak gem, paham 🤚."}
    ]

for message in st.session_state["messages"]:
    if message["role"] == "user":
        st.chat_message("user").write(f" {message['content']}")
    else:
        st.chat_message("Assistant").write(f" {message['content']}")

user_input = st.chat_input("Ketik pesan Anda:")

if user_input:

    st.session_state["messages"].append({"role": "user", "content": user_input})
    st.chat_message("User").write(f"{user_input}")

    try:
        # Create chat completion request
        response = client.chat.completions.create(
            model="meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo",
            messages=st.session_state["messages"],
            max_tokens=1000,
            temperature=0.7,
            top_p=0.9,
            top_k=50,
            repetition_penalty=1.1,
        )

        # Extract assistant's response
        if response and hasattr(response, "choices"):
            assistant_reply = response.choices[0].message.content.strip()
        else:
            assistant_reply = "Maaf, terjadi kesalahan pada respons model."

        # Modifikasi respons untuk menyertakan nama Kak Gem
        assistant_reply = f" {assistant_reply}"

        # Append assistant response to session state
        st.session_state["messages"].append({"role": "assistant", "content": assistant_reply})
        st.chat_message("Assistant").write(f" {assistant_reply}")

    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")
