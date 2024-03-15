import os
import re
from PIL import Image

import streamlit as st
from streamlit_lottie import st_lottie_spinner

from loading import loading_wait
from model import InputModel, RankingModel
from view import InputView, RankingView
from controller import InputController, RankingController

# 유튜브 아이콘 이미지 로드
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

st.set_page_config(**PAGE_CONFIG)


def main():

    # 모델 및 뷰 객체 생성
    input_model = InputModel()
    ranking_model = RankingModel()

    input_view = InputView()
    ranking_view = RankingView()

    # 컨트롤러 객체 생성
    input_controller = InputController(input_model, input_view)
    ranking_controller = RankingController(ranking_model, ranking_view)

    # 입력 데이터 수집
    input_controller.run()
    selected_country = input_model.get_selected_country()

    # 랭킹 데이터 로드 및 표시
    ranking_controller.load_ranking(selected_country)
    ranking_controller.display_ranking()

    # 선택한 분석 기능 처리
    selected_function = input_view.select_function_sidebar()
    if input_view.confirm_function_button():
        with st_lottie_spinner(loading_wait(), key="loading"):
            input_controller.handle_function(
                selected_function, ranking_model.get_ranking_df()
            )

    # 워드클라우드 생성 버튼 처리
    if input_view.generate_wordcloud_button():
        with st_lottie_spinner(loading_wait(), key="loading"):
            input_controller.display_wordcloud(ranking_model.get_ranking_df())

    id_pattern = re.compile("[A-Za-z0-9_-]{11}")

    # 동영상 댓글 분석 입력 처리
    input_video_id, analysis_btn = input_view.input_analysis_video()
    if analysis_btn:
        try:
            video_id = id_pattern.search(input_video_id).group()
            if video_id is not None:
                with st_lottie_spinner(loading_wait(), key="loading"):
                    ranking_view.video_comments_analysis(
                        ranking_controller.load_comments_analysis(video_id)
                    )
            else:
                input_view.input_invalid()
        except:
            input_view.input_invalid()

    compare_video_1, compare_video_2, compare_button = input_view.input_compare_videos()
    if compare_button:
        try:
            video_id_1 = id_pattern.search(compare_video_1).group()
            video_id_2 = id_pattern.search(compare_video_2).group()
            if video_id_1 is not None and video_id_2 is not None:
                with st_lottie_spinner(loading_wait(), key="loading"):
                    input_controller.compare_youtube_videos(
                        ranking_model.get_ranking_df(), compare_video_1, compare_video_2, ranking_controller
                    )
            else:
                input_view.input_invalid()
        except IndexError:
            input_view.input_country_change_error()
        except:
            input_view.input_invalid()


if __name__ == "__main__":
    main()