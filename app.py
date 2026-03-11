# app.py
import streamlit as st
from pptx import Presentation
from openai import OpenAI

st.set_page_config(page_title="AI Сабақ жоспары генераторы", layout="wide")
st.title("AI Сабақ жоспары генераторы")

# --- Streamlit форма ---
subject = st.text_input("Пән")
topic = st.text_input("Сабақ тақырыбы")
group = st.text_input("Группа")

# --- OpenAI клиенті ---
client = OpenAI()  # API key жүйеде орнатылған болуы керек

# --- AI арқылы слайд мәтінін генерациялау ---
def generate_slide_text(topic, subject):
    prompt = f"""
    Сабақ тақырыбы: {topic}
    Пән: {subject}
    
    6–8 слайдқа арналған мазмұн дайында. 
    Әр слайдта қысқаша мәтін: 
    - Тақырып атауы
    - Түсіндіру мәтіні
    Мәтін қазақша болсын.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# --- Презентация жасау функциясы ---
def create_ppt(topic, subject, slide_text):
    prs = Presentation()
    slides = slide_text.split("\n\n")  # әр жаңа параграф = жаңа слайд

    for s in slides:
        slide_layout = prs.slide_layouts[1]
        slide = prs.slides.add_slide(slide_layout)
        lines = s.split("\n")
        slide.shapes.title.text = lines[0] if len(lines) > 0 else "Слайд"
        slide.placeholders[1].text = "\n".join(lines[1:]) if len(lines) > 1 else ""

    prs.save("lesson.pptx")
    return "lesson.pptx"

# --- Батырма басылғанда ---
if st.button("AI арқылы презентация жасау"):
    if not subject or not topic:
        st.warning("Пән мен сабақ тақырыбын енгізіңіз!")
    else:
        with st.spinner("AI слайд мәтінін жасай жатыр..."):
            slide_text = generate_slide_text(topic, subject)

        st.subheader("Слайд мәтіні (тексеру үшін)")
        st.text_area("Слайд мәтінін қарап шығыңыз", slide_text, height=300)

        ppt_file = create_ppt(topic, subject, slide_text)

        st.success("Презентация дайын!")
        with open(ppt_file, "rb") as f:
            st.download_button(
                "Презентация жүктеу",
                f,
                file_name="lesson.pptx",
                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
            )
