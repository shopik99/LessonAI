import streamlit as st
from google import genai

# ====== Secrets.toml арқылы API кілтін алу ======
API_KEY = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=API_KEY)

# ====== Streamlit интерфейсі ======
st.set_page_config(page_title="Pourochny Plan Chat", page_icon="📚")
st.title("📚 Поурочный жоспар генераторы")

# Чат тарихы
if "messages" not in st.session_state:
    st.session_state.messages = []

# Пән атауы мен сабақ тақырыбы
subject = st.text_input("Пән атауы:")
topic = st.text_input("Сабақ тақырыбы:")

if st.button("Жоспар жасау") and subject and topic:
    # Пайдаланушы хабарын сақтау
    user_prompt = f"Маған '{subject}' пәні бойынша '{topic}' тақырыбына арналған поурочный сабақ жоспарын жаса, әр кезеңді сипаттап, тапсырмаларды көрсет."
    st.session_state.messages.append({"role": "user", "content": user_prompt})

    # Gemini API шақыру
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_prompt
        )
        plan_text = response.text
    except Exception as e:
        plan_text = f"Қате шықты: {e}"

    # API жауабын сақтау
    st.session_state.messages.append({"role": "assistant", "content": plan_text})

# Чат тарихын көрсету
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"**Сіз:** {msg['content']}")
    else:
        st.markdown(f"**Gemini:** {msg['content']}")
