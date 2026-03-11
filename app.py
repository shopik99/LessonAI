import streamlit as st
from google import genai

# ====== Secrets.toml арқылы API кілтін алу ======
API_KEY = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=API_KEY)

st.set_page_config(page_title="Презентация генераторы", page_icon="🖼️")
st.title("🖼️ Презентация генераторы (GPT/Gemini)")

# Чат тарихы
if "slides" not in st.session_state:
    st.session_state.slides = []

# Пән және сабақ тақырыбы
subject = st.text_input("Пән атауы:")
topic = st.text_input("Сабақ тақырыбы:")

num_slides = st.number_input("Слайд саны:", min_value=3, max_value=10, value=5, step=1)

if st.button("Презентация жасау") and subject and topic:
    # Пайдаланушы сұранысын сақтау
    prompt = f"Маған '{subject}' пәні бойынша '{topic}' тақырыбында {num_slides} слайдтық презентация жаса. Әр слайдқа қысқаша тақырып пен сипаттама бер."
    st.session_state.slides.append({"role": "user", "content": prompt})

    # Gemini API шақыру
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        slides_text = response.text
    except Exception as e:
        slides_text = f"Қате шықты: {e}"

    st.session_state.slides.append({"role": "assistant", "content": slides_text})

# Слайдтарды көрсету
for msg in st.session_state.slides:
    if msg["role"] == "assistant":
        st.markdown("### 📑 Генерацияланған презентация мазмұны")
        # Слайдтарды жол бойынша бөліп көрсету
        for line in msg["content"].split("\n"):
            if line.strip():
                st.markdown(f"- {line.strip()}")
