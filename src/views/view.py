import re
import streamlit as st
from config.country_code import COUNTRIES
from config.analysis_options import ANALYSIS_OPTIONS
from config.country_code import country_to_country_code
from utils.loading import loading_wait


from streamlit_echarts import st_echarts
from streamlit_lottie import st_lottie_spinner


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
            analysis_option, result = controller.analyze_youtube_by_option(
                selected_option
            )
            display_youtube_analysis(analysis_option, result)

    if st.sidebar.button("워드클라우드 생성", use_container_width=True):
        with st_lottie_spinner(loading_wait(), key="loading"):
            result = controller.generate_wordcloud()
            display_youtube_wordcloud(result)

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
        try:
            comments_analysis_video_id = video_id_pattern.search(
                comments_analysis_video_id
            ).group()
            if comments_analysis_video_id is not None:
                with st_lottie_spinner(loading_wait(), key="loading"):
                    result, positive_comments, negative_comments, video_id = (
                        controller.analyze_comments(comments_analysis_video_id)
                    )
                    display_comments_analysis(
                        result, positive_comments, negative_comments, video_id
                    )
                    # 베타 버전 욕설 감지 추가
                    warning = controller.analyze_slang_beta(comments_analysis_video_id)
                    display_slang_beta_version_function(warning)
            else:
                st.sidebar.warning("유효한 동영상ID를 입력해주세요.")
        except:
            st.sidebar.warning("유효한 동영상ID를 입력해주세요.")

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
        try:
            comparison_video_id1 = video_id_pattern.search(
                comparison_video_id1_input
            ).group()
            comparison_video_id2 = video_id_pattern.search(
                comparison_video_id2_input
            ).group()
            if comparison_video_id1 is not None and comparison_video_id2 is not None:
                with st_lottie_spinner(loading_wait(), key="loading"):
                    (
                        result,
                        video1_comments_result,
                        video2_comments_result,
                        chart1,
                        chart2,
                    ) = controller.compare_youtube_videos(
                        comparison_video_id1, comparison_video_id2
                    )
                    display_youtube_comparison(
                        result,
                        video1_comments_result,
                        video2_comments_result,
                        chart1,
                        chart2,
                    )
            else:
                st.sidebar.warning("유효한 동영상ID를 입력해주세요.")
        except IndexError:
            st.warning("동영상ID를 지우고 다시 입력해주세요.")
        except:
            st.sidebar.warning("유효한 동영상ID를 입력해주세요.")


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


def display_youtube_analysis(analysis_option, result):
    st.markdown(
        f"<h1 style='text-align: center;'>{analysis_option}</h1>",
        unsafe_allow_html=True,
    )
    st.divider()
    if analysis_option == ANALYSIS_OPTIONS[0]:
        st_echarts(options=result[0], height="500px")
        st.markdown(result[1])
    elif analysis_option == ANALYSIS_OPTIONS[1]:
        st_echarts(options=result[0], height="500px")
        st.markdown(result[1])
    elif analysis_option == ANALYSIS_OPTIONS[2]:
        st.markdown(
            f"<h3 style='text-align: center;'>TOP 200 인기 동영상들은 평균 {result}개의 태그를 사용합니다.</h3>",
            unsafe_allow_html=True,
        )


def display_youtube_wordcloud(result):
    st.markdown(
        "<h1 style='text-align: center;'>인기 있는 주제와 키워드</h1>",
        unsafe_allow_html=True,
    )
    st.divider()
    st.image(result[0], caption="현재 유튜브에서 인기있는 주제")
    st.markdown(result[1])


def display_comments_analysis(result, positive_comments, negative_comments, video_id):
    positive_result = result[0]
    negative_result = result[1]
    st.markdown(
        "<h1 style='text-align: center;'>유튜브 댓글 분석</h1>",
        unsafe_allow_html=True,
    )
    st.divider()
    st.video(f"https://www.youtube.com/watch?v={video_id}")
    st.write("해당 동영상의 댓글의 반응은")
    st.subheader(f"긍정적인 반응😃: {2 * positive_result}%")
    positive = st.expander("긍정적인 댓글")
    positive.write(positive_comments)

    st.subheader(f"부정적인 반응🤬: {2 * negative_result}%")
    negative = st.expander("부정적인 댓글")
    negative.write(negative_comments)
    st.write("의 반응을 보입니다.")


def display_slang_beta_version_function(result):
    st.divider()
    st.markdown(
        "<h1 style='font-style: italic; color:red;'>Beta 버전</h1>",
        unsafe_allow_html=True,
    )
    beta_version = st.expander("베타 버전 기능입니다.")
    beta_version.markdown(
        "#### **해당 동영상에서 사용된 욕설의 횟수는 {0}회입니다.**".format(result)
    )
    if result > 20:
        beta_version.warning(
            "이 동영상은 어린아이들이 시청하기에 다소 부적절할 수 있습니다."
        )
    else:
        beta_version.info("이 동영상은 어린아이들이 시청하기에 적합합니다.")


def display_youtube_comparison(
    result, video1_comments_result, video2_comments_result, chart1, chart2
):

    video1_comments_analysis = video1_comments_result[0]
    video1_comments = video1_comments_result[1]

    video2_comments_analysis = video2_comments_result[0]
    video2_comments = video2_comments_result[1]

    st.markdown(
        "<h1 style='text-align: center;'>유튜브 동영상 비교</h1>",
        unsafe_allow_html=True,
    )
    st.divider()
    col1, col2 = st.columns(2)

    col1.subheader(result[0]["채널명"])
    col1.markdown(
        "```조회수 {0:,}회 / {1} {2}```".format(
            result[0]["조회수"], result[0]["업로드날짜"], result[0]["업로드요일"]
        )
    )
    col1.video(result[0]["동영상링크"])
    col1.markdown("> {0}".format(result[0]["제목"]))
    col1.markdown(
        "```좋아요 {0:,}개 / 댓글 {1:,}개 / {2}```".format(
            result[0]["좋아요 수"], result[0]["댓글 수"], result[0]["카테고리"]
        )
    )
    video1_tags = col1.expander("사용한 태그")
    video1_tags.write(result[0]["태그"])
    col1.markdown(
        "댓글은 긍정적인 반응 {0}%, 부정적인 반응 {1}% 입니다.".format(
            video1_comments_analysis[0], video1_comments_analysis[1]
        )
    )

    col2.subheader(result[1]["채널명"])
    col2.markdown(
        "```조회수 {0:,}회 / {1} {2}```".format(
            result[1]["조회수"], result[1]["업로드날짜"], result[1]["업로드요일"]
        )
    )
    col2.video(result[1]["동영상링크"])
    col2.markdown("> {0}".format(result[1]["제목"]))
    col2.markdown(
        "```좋아요 {0:,}개 / 댓글 {1:,}개 / {2}```".format(
            result[1]["좋아요 수"], result[1]["댓글 수"], result[1]["카테고리"]
        )
    )

    video2_tags = col2.expander("사용한 태그")
    video2_tags.write(result[1]["태그"])
    col2.markdown(
        "댓글은 긍정적인 반응 {0}%, 부정적인 반응 {1}% 입니다.".format(
            video2_comments_analysis[0], video2_comments_analysis[1]
        )
    )

    st.divider()

    comments_pie_chart_col, likes_pie_chart_col = st.columns(2)
    with comments_pie_chart_col:
        st_echarts(options=chart1)

    with likes_pie_chart_col:
        st_echarts(options=chart2)

    st.divider()

    st.subheader(f"{result[0]['제목']} | 댓글 여론")
    video1_positive_comments = st.expander("긍정적인 댓글")
    video1_positive_comments.write(video1_comments[0])
    video1_negative_comments = st.expander("부정적인 댓글")
    video1_negative_comments.write(video1_comments[1])

    st.divider()

    st.subheader(f"{result[1]['제목']} | 댓글 여론")
    video2_positive_comments = st.expander("긍정적인 댓글")
    video2_positive_comments.write(video2_comments[0])
    video2_negative_comments = st.expander("부정적인 댓글")
    video2_negative_comments.write(video2_comments[1])
