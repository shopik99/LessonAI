import streamlit as st
from google import genai
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from io import BytesIO
import requests
from pptx.enum.text import PP_ALIGN

# ====== Secrets.toml арқылы API кілтін алу ======
API_KEY = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=API_KEY)

st.set_page_config(page_title="Толық презентация генератор", page_icon="🎓")
st.title("🎓 Толық теориялық презентация генераторы")

# Пайдаланушыдан пән, тақырып және слайд саны
subject = st.text_input("Пән атауы:")
topic = st.text_input("Сабақ тақырыбы:")
num_slides = st.number_input("Слайд саны:", min_value=3, max_value=10, value=5, step=1)

if st.button("Презентация жасау") and subject and topic:
    prompt = f"""Маған '{subject}' пәні бойынша '{topic}' тақырыбында {num_slides} слайдтық презентация жаса. 
    Әр слайдқа:
    1) тақырып (қазақша)
    2) теориялық мәтін
    3) негізгі пункттер (bullet)
    Қысқа әрі түсінікті болсын, әр слайд бөлек жолға шығсын."""

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
        prs = Presentation()
        background_colors = [(240, 248, 255), (255, 248, 220), (245, 255, 250), (255, 240, 245)]
        sample_images = [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/School_books.jpg/320px-School_books.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1f/Blackboard.jpg/320px-Blackboard.jpg"
        ]

        slide_index = 0
        for slide_line in slides_text.split("\n"):
            slide_line = slide_line.strip()
            if not slide_line:
                continue

            # Слайд тақырыбы + мәтінді бөліп алу
            if ":" in slide_line:
                parts = slide_line.split(":", 1)
                slide_title = parts[0].strip()
                slide_content = parts[1].strip()
            else:
                slide_title = slide_line
                slide_content = ""

            slide = prs.slides.add_slide(prs.slide_layouts[1])
            slide.shapes.title.text = slide_title

            # Фон түсі
            fill = slide.background.fill
            color = background_colors[slide_index % len(background_colors)]
            fill.solid()
            fill.fore_color.rgb = RGBColor(*color)

            # Мәтінді бірнеше paragraph-қа бөлу
            textbox = slide.placeholders[1]
            textbox.text = ""
            for bullet in slide_content.split(". "):
                p = textbox.text_frame.add_paragraph()
                p.text = bullet.strip()
                p.level = 0
                p.font.size = Pt(18)
                p.font.color.rgb = RGBColor(0,0,0)
                p.alignment = PP_ALIGN.LEFT

            # Сурет қосу
            img_url = sample_images[slide_index % len(sample_images)]
            try:
                img_data = requests.get(img_url).content
                slide.shapes.add_picture(BytesIO(img_data), Inches(5.5), Inches(1.5), width=Inches(3))
            except:
                pass

            slide_index += 1

        # PPTX файлды байтқа жазу
        pptx_bytes = BytesIO()
        prs.save(pptx_bytes)
        pptx_bytes.seek(0)

        st.success("🎉 Презентация дайын!")
        st.download_button(
            label="📥 PPTX жүктеу",
            data=pptx_bytes,
            file_name=f"{topic}_presentation.pptx",
            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
        )
