import os
from PIL import Image
import streamlit as st

def set_page_config():
    icon = Image.open(
        os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "assets", "youtube.png")
        )
    )
    
    page_config = {
        "page_title": "유튜브 트렌드 대시보드",
        "page_icon": icon,
        "layout": "centered",
        "initial_sidebar_state": "auto",
    }
    
    st.set_page_config(**page_config)