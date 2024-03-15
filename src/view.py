import os
import json
import streamlit as st
from matplotlib import rc

# 한글 폰트 설정
rc("font", family="AppleGothic")


class InputView:

    COUNTRIES = [
        "대한민국",
        "일본",
        "미국",
        "캐나다",
        "영국",
        "독일",
        "프랑스",
        "인도",
        "러시아",
        "브라질",
        "호주",
        "이탈리아",
        "스페인",
        "멕시코",
        "스웨덴",
        "네덜란드",
        "터키",
        "뉴질랜드",
        "아르헨티나",
        "폴란드",
        "남아프리카 공화국",
    ]

    # 국가 선택 사이드바 표시
    def select_country_sidebar(self):
        st.sidebar.title("유튜브 분석")
        selected_country = st.sidebar.selectbox("국가 선택", self.COUNTRIES)
        with open(
            os.path.abspath(
                os.path.join(
                    os.path.dirname(__file__), "..", "data", "country_code.json"
                )
            ),
            "r",
        ) as f:
            country_codes = json.load(f)
        return country_codes[selected_country]

    # 분석 방식 선택 사이드바 표시
    def select_function_sidebar(self):
        OPTIONS = [
            "요일별 인기 동영상 업로드 비율",
            "시간대별 인기 동영상 업로드 비율",
            "인기 동영상 평균 태그 갯수",
        ]
        selected_option = st.sidebar.selectbox(
            "분석 방식", OPTIONS, index=None, placeholder="분석 방식을 선택해주세요."
        )
        return selected_option

    # 분석 실행 버튼 표시
    def confirm_function_button(self):
        return st.sidebar.button("분석 실행하기", use_container_width=True)

    # 워드클라우드 생성 버튼 표시
    def generate_wordcloud_button(self):
        return st.sidebar.button("워드클라우드 생성", use_container_width=True)

    # 워드클라우드 및 챗봇 응답 표시
    def display_wordcloud(self, wordcloud, response):
        st.image(wordcloud, caption="인기 동영상 제목 워드클라우드")
        st.markdown(response)

    # 분석 결과 표시
    def result_by_function(self, function_code, data):
        if function_code == "요일별 인기 동영상 업로드 비율":
            return (
                st.write(function_code),
                st.bar_chart(data[0], use_container_width=True),
                st.markdown(data[1]),
            )
        elif function_code == "시간대별 인기 동영상 업로드 비율":
            return (
                st.write(function_code),
                st.bar_chart(data[0], use_container_width=True),
                st.markdown(data[1]),
            )
        elif function_code == "인기 동영상 평균 태그 갯수":
            return st.subheader(
                f"TOP 200 인기 동영상들은 평균 {data}개의 태그를 사용합니다."
            )

    # 동영상 댓글 분석 입력 UI 표시
    def input_analysis_video(self):
        st.sidebar.title("유튜브 댓글 분석")
        col1, col2 = st.sidebar.columns(2)

        return (
            col1.text_input(
                "동영상 분석",
                placeholder="동영상ID 입력",
                label_visibility="collapsed",
                value=None,
            ),
            col2.button("분석", use_container_width=True),
        )

    # 유효하지 않은 동영상 ID 입력 경고 표시
    def input_invalid(self):
        return st.sidebar.warning("유효한 동영상ID를 입력해주세요.")

    def input_compare_videos(self):
        st.sidebar.title("유튜브 비교")
        col1, col2, col3 = st.sidebar.columns((8, 2, 8))
        col2.write("&nbsp;VS")
        return (
            col1.text_input(
                "동영상 A",
                placeholder="동영상ID 입력",
                label_visibility="collapsed",
                value=None,
            ),
            col3.text_input(
                "동영상 B",
                placeholder="동영상ID 입력",
                label_visibility="collapsed",
                value=None,
            ),
            st.sidebar.button("비교하기", use_container_width=True),
        )

    def display_compare_results(self, data, comments_result1, comments_result2):

        st.markdown(
            "<h1 style='text-align: center;'>유튜브 동영상 비교</h1>",
            unsafe_allow_html=True,
        )
        col1, col2 = st.columns(2)

        col1.subheader(data[0]["채널명"])
        col1.markdown(
            "```조회수 {0:,}회 / {1} {2}```".format(
                data[0]["조회수"], data[0]["업로드날짜"], data[0]["업로드요일"]
            )
        )
        col1.video(data[0]["동영상링크"])
        col1.markdown("> {0}".format(data[0]["제목"]))

        col1.markdown(
            "```좋아요 {0:,}개 / 댓글 {1:,}개```".format(
                data[0]["좋아요수"], data[0]["댓글수"]
            )
        )
        col1.markdown(
            "댓글은 긍정적인 반응 {0}%, 부정적인 반응 {1}% 입니다.".format(
                comments_result1[0], comments_result1[1]
            )
        )


        col2.subheader(data[1]["채널명"])
        col2.markdown(
            "```조회수 {0:,}회 / {1} {2}```".format(
                data[1]["조회수"], data[1]["업로드날짜"], data[1]["업로드요일"]
            )
        )
        col2.video(data[1]["동영상링크"])
        col2.markdown("> {0}".format(data[1]["제목"]))

        col2.markdown(
            "```좋아요 {0:,}개 / 댓글 {1:,}개```".format(
                data[1]["좋아요수"], data[1]["댓글수"]
            )
        )
        col2.markdown(
            "댓글은 긍정적인 반응 {0}%, 부정적인 반응 {1}% 입니다.".format(
                comments_result2[0], comments_result2[1]
            )
        )

    # 국가 변경 후 유튜브 비교 시 동영상 ID를 그대로 뒀을 때 에러 발생 할 경우 경고
    def input_country_change_error(self):
        return st.warning("동영상ID를 지우고 다시 입력해주세요.")

class RankingView:

    # 데이터프레임을 특정 크기의 페이지로 나누는 함수
    def split_dataframe(self, input_df, rows):
        return [
            input_df.loc[i : i + rows - 1, :] for i in range(0, len(input_df), rows)
        ]

    # 랭킹 데이터 표시
    def display_ranking(self, ranking_df) -> None:

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
                sort_field = st.selectbox("정렬 기준", options=ranking_df.columns)

            with top_menu[2]:
                sort_direction = st.radio(
                    "오름차순 / 내림차순", options=["⬆️", "⬇️"], horizontal=True
                )

            # 데이터 정렬
            ranking_df = ranking_df.sort_values(
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
            total_pages = len(ranking_df) // batch_size
            current_page = st.number_input(
                "페이지", min_value=1, max_value=total_pages, step=1
            )

        # 현재 페이지 번호 표시
        with bottom_menu[0]:
            st.markdown(f"페이지 **{current_page}** / **{total_pages}** ")

        # 데이터프레임을 페이지별로 분할하여 표시
        pages = self.split_dataframe(ranking_df, batch_size)
        pagination.dataframe(data=pages[current_page - 1], use_container_width=True)

    # 동영상 댓글 분석 결과 표시
    def video_comments_analysis(self, data):
        positive = data[1][0]
        negative = data[1][1]
        return (
            st.video(f"https://www.youtube.com/watch?v={data[0]}"),
            st.write("해당 동영상의 댓글의 반응은"),
            st.subheader(f"긍정적인 반응😃: {2 * positive}%"),
            st.subheader(f"부정적인 반응🤬: {2 * negative}%"),
            st.write("의 반응을 보입니다."),
        )

