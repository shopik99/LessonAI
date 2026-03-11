import streamlit as st
from google import genai
from pptx import Presentation
from pptx.util import Inches, Pt
from io import BytesIO

# ====== Secrets.toml арқылы API кілтін алу ======
API_KEY = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=API_KEY)

st.set_page_config(page_title="Презентация генераторы", page_icon="🖼️")
st.title("📑 GPT/Gemini негізіндегі презентация генераторы")

# Пайдаланушыдан пән, тақырып және слайд санын алу
subject = st.text_input("Пән атауы:")
topic = st.text_input("Сабақ тақырыбы:")
num_slides = st.number_input("Слайд саны:", min_value=3, max_value=10, value=5, step=1)

if st.button("Презентация жасау") and subject and topic:
    # GPT сұранысы
    prompt = f"Маған '{subject}' пәні бойынша '{topic}' тақырыбында {num_slides} слайдтық презентация жасаңдар. Әр слайдқа тақырып пен қысқаша мәтін беріңдер, әр слайд бөлек жолға."
    
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        slides_text = response.text
    except Exception as e:
        st.error(f"GPT сұранысында қате: {e}")
        slides_text = None

    if slides_text:
        # PPTX презентация жасау
        prs = Presentation()
        for slide_line in slides_text.split("\n"):
            slide_line = slide_line.strip()
            if not slide_line:
                continue
            # Әдетте: "Слайд 1: Тақырып – Мәтін" форматында келеді
            if ":" in slide_line:
                parts = slide_line.split(":", 1)
                slide_title = parts[0].strip()
                slide_content = parts[1].strip()
            else:
                slide_title = slide_line
                slide_content = ""
            slide = prs.slides.add_slide(prs.slide_layouts[1])  # Тақырып + мәтін
            slide.shapes.title.text = slide_title
            slide.placeholders[1].text = slide_content

        # PPTX файлды байтқа жазу (Streamlit жүктеу үшін)
        pptx_bytes = BytesIO()
        prs.save(pptx_bytes)
        pptx_bytes.seek(0)

        # Жүктеу батырмасы
        st.success("Презентация дайын! Төменнен жүктеп алыңыз:")
        st.download_button(
            label="📥 PPTX жүктеу",
            data=pptx_bytes,
            file_name=f"{topic}_presentation.pptx",
            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
        )
