import re
import streamlit as st
from country_code import COUNTRIES
from country_code import country_to_country_code
from loading import loading_wait

from streamlit_echarts import st_echarts
from streamlit_lottie import st_lottie_spinner

ANALYSIS_OPTIONS = [
    "요일별 인기 동영상 업로드 비율",
    "시간대별 인기 동영상 업로드 비율",
    "인기 동영상 평균 태그 갯수",
]


def display_sidebar(controller):
    st.sidebar.title("유튜브 분석")
    selected_country = st.sidebar.selectbox("국가 선택", COUNTRIES)
    # 국가 선택과 분석 방식 선택
    country_code = country_to_country_code(selected_country)
    ranking_df = controller.get_popular_videos_data(country_code)

    display_youtube_ranking_board(ranking_df)

    selected_option = st.sidebar.selectbox(
        "분석 방식",
        ANALYSIS_OPTIONS,
        index=None,
        placeholder="분석 방식을 선택해주세요.",
    )

    if st.sidebar.button("분석 실행하기", use_container_width=True):
        with st_lottie_spinner(loading_wait(), key="loading"):
            youtube_analysis_result = controller.analyze_youtube_by_option(
                selected_option
            )

    if st.sidebar.button("워드클라우드 생성", use_container_width=True):
        with st_lottie_spinner(loading_wait(), key="loading"):
            youtube_analysis_wordcloud = controller.generate_wordcloud()
            display_youtube_wordcloud(youtube_analysis_wordcloud)

    st.sidebar.title("유튜브 댓글 분석")
    comments_analysis_col1, comments_analysis_col2 = st.sidebar.columns(2)

    comments_analysis_video_id = comments_analysis_col1.text_input(
        "동영상 분석",
        placeholder="동영상ID 입력",
        label_visibility="collapsed",
        value=None,
    )

    video_id_pattern = re.compile("[A-Za-z0-9_-]{11}")

    if comments_analysis_col2.button("분석", use_container_width=True):
        comments_analysis_video_id = video_id_pattern.search(
            comments_analysis_video_id
        ).group()
        if comments_analysis_video_id is not None:
            with st_lottie_spinner(loading_wait(), key="loading"):
                comments_analysis_result = controller.analyze_comments(
                    comments_analysis_video_id
                )
                display_comments_analysis(comments_analysis_result)
                # 베타 버전 욕설 감지 추가
        else:
            pass  # 유효하지 않음 처리

    st.sidebar.title("유튜브 비교")
    comparison_col1, comparison_col2, comparison_col3 = st.sidebar.columns((8, 2, 8))

    comparison_col2.markdown(
        "<h3 style='text-align: center;'>VS</h3>", unsafe_allow_html=True
    )
    comparison_video_id1_input = comparison_col1.text_input(
        "동영상 A",
        placeholder="동영상ID 입력",
        label_visibility="collapsed",
        value=None,
    )
    comparison_video_id2_input = comparison_col3.text_input(
        "동영상 B",
        placeholder="동영상ID 입력",
        label_visibility="collapsed",
        value=None,
    )
    
    if st.sidebar.button("비교하기", use_container_width=True):
        
        comparison_video_id1 = video_id_pattern.search(comparison_video_id1_input).group()
        comparison_video_id2 = video_id_pattern.search(comparison_video_id2_input).group()
        if comparison_video_id1 is not None and comparison_video_id2 is not None:
            with st_lottie_spinner(loading_wait(), key="loading"):
                controller.compare_youtube_videos(comparison_video_id1, comparison_video_id2)
        else:
            pass # 예외처리
        

    # controller.

    # analysis_type = st.sidebar.selectbox("분석 방식", controller.get_analysis_options())

    # # 분석 실행하기 버튼
    # if st.sidebar.button("분석 실행하기"):
    #     result = controller.run_analysis(country, analysis_type)
    #     display_analysis_results(result)

    # st.sidebar.title("유튜브 댓글 분석")
    # video_id = st.sidebar.text_input("동영상ID 입력", "")

    # # 댓글 분석 버튼
    # if st.sidebar.button("댓글 분석"):
    #     comments_result = controller.analyze_comments(video_id)
    #     display_comments_analysis(comments_result)


def display_youtube_ranking_board(result):
    st.markdown(
        "<h1 style='text-align: center;'>유튜브 트렌드 대시보드</h1>",
        unsafe_allow_html=True,
    )
    top_menu = st.columns(3)

    # 정렬 옵션 표시
    with top_menu[0]:
        sort = st.radio("정렬하기", options=["Yes", "No"], horizontal=1, index=1)

    # 정렬이 선택된 경우 정렬 옵션 표시
    if sort == "Yes":
        with top_menu[1]:
            sort_field = st.selectbox("정렬 기준", options=result.columns)

        with top_menu[2]:
            sort_direction = st.radio(
                "오름차순 / 내림차순", options=["⬆️", "⬇️"], horizontal=True
            )

        # 데이터 정렬
        result = result.sort_values(
            by=sort_field, ascending=sort_direction == "⬆️", ignore_index=True
        )

    # 페이지네이션 설정
    pagination = st.container()
    bottom_menu = st.columns((4, 1, 1))

    # 한 페이지에 보여질 항목 수 선택
    with bottom_menu[2]:
        batch_size = st.selectbox("갯수", options=[25, 50, 100])

    # 현재 페이지 및 전체 페이지 수 설정
    with bottom_menu[1]:
        total_pages = len(result) // batch_size
        current_page = st.number_input(
            "페이지", min_value=1, max_value=total_pages, step=1
        )

    # 현재 페이지 번호 표시
    with bottom_menu[0]:
        st.markdown(f"페이지 **{current_page}** / **{total_pages}** ")

    # 데이터프레임을 페이지별로 분할하여 표시
    pages = [
        result.loc[i : i + batch_size - 1, :] for i in range(0, len(result), batch_size)
    ]
    pagination.dataframe(data=pages[current_page - 1], use_container_width=True)


def display_youtube_analysis(display_code, result):
    if display_code == 1:
        pass
    if display_code == 2:
        pass
    if display_code == 3:
        pass


def display_youtube_wordcloud(result):
    pass


def display_comments_analysis(result):
    pass


def display_beta_version_function(result):
    pass


def display_youtube_comparison(comments_result):
    pass
