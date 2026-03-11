import streamlit as st
from google import genai

# ====== Secrets.toml арқылы API кілтін алу ======
API_KEY = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=API_KEY)

# ====== Streamlit интерфейсі ======
st.set_page_config(page_title="Gemini Chat", page_icon="🤖")
st.title("🤖 Google Gemini Chat")

# Чат тарихын сақтау
if "messages" not in st.session_state:
    st.session_state.messages = []

# Пайдаланушыдан сұрақ алу
user_input = st.text_input("Сұрағыңызды енгізіңіз:")

if st.button("Жіберу") and user_input:
    # Пайдаланушы хабарын сақтау
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Gemini API шақыру
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",  # қолжетімді модель
            contents=user_input
        )
        gemini_reply = response.text
    except Exception as e:
        gemini_reply = f"Қате шықты: {e}"

    # API жауабын сақтау
    st.session_state.messages.append({"role": "assistant", "content": gemini_reply})

# Чат тарихын көрсету
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"**Сіз:** {msg['content']}")
    else:
        st.markdown(f"**Gemini:** {msg['content']}")
