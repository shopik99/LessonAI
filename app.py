import streamlit as st
from pptx import Presentation


# ---- Презентация жасау функциясы ----
def create_presentation(topic, subject):

    prs = Presentation()

    # 1 слайд (титул)
    slide_layout = prs.slide_layouts[0]
    slide = prs.slides.add_slide(slide_layout)

    slide.shapes.title.text = topic
    slide.placeholders[1].text = subject


    # 2 слайд
    slide_layout = prs.slide_layouts[1]
    slide = prs.slides.add_slide(slide_layout)

    slide.shapes.title.text = "Сабақ мақсаты"
    slide.placeholders[1].text = "Студенттер тақырыпты түсінеді"


    # 3 слайд
    slide = prs.slides.add_slide(slide_layout)

    slide.shapes.title.text = "Негізгі бөлім"
    slide.placeholders[1].text = "Тақырып бойынша негізгі түсіндіру"


    # 4 слайд
    slide = prs.slides.add_slide(slide_layout)

    slide.shapes.title.text = "Қорытынды"
    slide.placeholders[1].text = "Сабақ қорытындысы"


    prs.save("lesson.pptx")

    return "lesson.pptx"


# ---- Streamlit интерфейсі ----

st.title("AI Сабақ жоспары генераторы")

subject = st.text_input("Пән")
topic = st.text_input("Сабақ тақырыбы")
group = st.text_input("Группа")

if st.button("Презентация жасау"):

    ppt_file = create_presentation(topic, subject)

    st.success("Презентация дайын!")

    with open(ppt_file, "rb") as f:
        st.download_button(
            label="Презентация жүктеу",
            data=f,
            file_name="lesson.pptx",
            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
        )
