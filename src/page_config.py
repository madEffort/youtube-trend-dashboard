# 유튜브 아이콘 이미지 로드
import os
from PIL import Image
import streamlit as st

ICON = Image.open(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "assets", "youtube.png")
    )
)

# Streamlit 페이지 설정
PAGE_CONFIG = {
    "page_title": "유튜브 트렌드 대시보드",
    "page_icon": ICON,
    "layout": "centered",
    "initial_sidebar_state": "auto",
}

def init_setting():
    st.set_page_config(**PAGE_CONFIG)


def main():
    init_setting()

if __name__ == "__main__":
    main()