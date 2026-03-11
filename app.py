import streamlit as st
import requests
import json

st.set_page_config(page_title="Canva презентация генератор", page_icon="🎓")
st.title("🎓 Canva арқылы презентация генератор")

# Secrets‑тен Client ID / Secret алу
CLIENT_ID = st.secrets["CANVA_CLIENT_ID"]
CLIENT_SECRET = st.secrets["CANVA_CLIENT_SECRET"]
REDIRECT_URI = st.secrets.get("CANVA_REDIRECT_URI", "https://shopikai.streamlit.app/oauth_callback")

st.markdown("""
**Қалай жұмыс істейді:**  
1️⃣ Canva Developer Portal‑дан Client ID / Client Secret және Access Token алыңыз  
2️⃣ Тақырып енгізіңіз  
3️⃣ “Презентация жасау” батырмасын басыңыз
""")

# Пайдаланушыдан тақырып енгізу
topic = st.text_input("Презентация тақырыбы:")

# Access Token енгізу
access_token = st.text_input("Canva Access Token:", type="password")

if st.button("Презентация жасау") and topic and access_token:
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    # 1️⃣ Жаңа дизайн жасау
    design_data = {
        "name": topic,
        "type": "presentation"
    }

    resp = requests.post("https://api.canva.com/v1/designs", headers=headers, data=json.dumps(design_data))
    if resp.status_code != 201:
        st.error(f"Қате дизайн жасау кезінде: {resp.text}")
    else:
        design_id = resp.json().get("id")
        st.success(f"Жаңа презентация жасалды! Design ID: {design_id}")

        # 2️⃣ Экспорт жасау
        export_url = f"https://api.canva.com/v1/designs/{design_id}/export"
        export_data = {
            "format": "pdf"  # немесе "pptx"
        }

        export_resp = requests.post(export_url, headers=headers, data=json.dumps(export_data))
        if export_resp.status_code == 200:
            file_url = export_resp.json().get("url")
            st.markdown(f"[📥 Жүктеу презентация]({file_url})")
        else:
            st.error(f"Экспортта қате: {export_resp.text}")
