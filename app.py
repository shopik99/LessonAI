import streamlit as st

st.title("AI Сабақ жоспарын генерациялау")

subject = st.text_input("Пән")
topic = st.text_input("Сабақ тақырыбы")
group = st.text_input("Группа")

if st.button("Генерациялау"):

    lesson = f"""
    Пән: {subject}
    Тақырып: {topic}
    Топ: {group}

    Сабақ кезеңдері:
    1. Ұйымдастыру
    2. Жаңа тақырып
    3. Практика
    4. Қорытынды
    """

    st.subheader("Сабақ жоспары")
    st.write(lesson)
