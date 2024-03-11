# view.py
from matplotlib import rc
import streamlit as st
import os
import json

rc('font', family='AppleGothic')

class InputView:

    COUNTRIES = [
        "대한민국", "일본", "미국", "캐나다", "영국", "독일", "프랑스", "인도", "러시아",
        "브라질", "호주", "이탈리아", "스페인", "멕시코", "스웨덴", "네덜란드", "터키",
        "뉴질랜드", "아르헨티나", "폴란드", "남아프리카 공화국"
    ]

    def select_country_sidebar(self):
        st.sidebar.title("데이터 분석")
        
        selected_country = st.sidebar.selectbox("국가 선택", self.COUNTRIES)
        with open(os.path.abspath("../data/country_code.json"), "r") as f:
            country_codes = json.load(f)

        return country_codes[selected_country]
    
    def select_function_sidebar(self):
        OPTIONS = ["요일별 인기 동영상 업로드 비율", "시간대별 인기 동영상 업로드 비율", "Option 3"]
        selected_option = st.sidebar.selectbox("분석 방식", OPTIONS, index=None, placeholder="분석 방식을 선택해주세요.")
        return selected_option

    def confirm_function_button(self):
        return st.sidebar.button("분석 실행하기", use_container_width=True)
    
    def generate_wordcloud_button(self):
        return st.sidebar.button("워드클라우드 생성", use_container_width=True)
    
    def result_by_function(self, function_code, data):
        if function_code == "요일별 인기 동영상 업로드 비율":
            return st.bar_chart(data, use_container_width=True)
        elif function_code == "시간대별 인기 동영상 업로드 비율":
            return st.bar_chart(data, use_container_width=True)
        elif function_code == "":
            pass

class RankingView:

    def split_dataframe(self, input_df, rows):
        return [input_df.loc[i:i+rows-1, :] for i in range(0, len(input_df), rows)]

    def display_ranking(self, ranking_df) -> None:
        st.title("유튜브 트렌드 대시보드")
        top_menu = st.columns(3)
        with top_menu[0]:
            sort = st.radio("정렬하기", options=["Yes", "No"], horizontal=1, index=1)

        if sort == "Yes":
            with top_menu[1]:
                sort_field = st.selectbox("정렬 기준", options=ranking_df.columns)

            with top_menu[2]:
                sort_direction = st.radio(
                    "오름차순 / 내림차순", options=["⬆️", "⬇️"], horizontal=True
                )

            ranking_df = ranking_df.sort_values(
                by=sort_field, ascending=sort_direction == "⬆️", ignore_index=True
            )

        pagination = st.container()

        bottom_menu = st.columns((4, 1, 1))

        with bottom_menu[2]:
            batch_size = st.selectbox("갯수", options=[25, 50, 100])

        with bottom_menu[1]:
            total_pages = (len(ranking_df) // batch_size)
            current_page = st.number_input(
                "페이지", min_value=1, max_value=total_pages, step=1
            )

        with bottom_menu[0]:
            st.markdown(f"페이지 **{current_page}** / **{total_pages}** ")

        pages = self.split_dataframe(ranking_df, batch_size)
        pagination.dataframe(data=pages[current_page - 1], use_container_width=True)

class AnalysisView:
    
    def display_wordcloud(self, wordcloud):
        st.image(wordcloud, caption='인기 동영상 제목 워드클라우드')