import streamlit as st
import os
import json

class InputView:

    COUNTRIES = [
        "대한민국", "일본", "미국", "캐나다", "영국", "독일", "프랑스", "인도", "러시아",
        "브라질", "호주", "이탈리아", "스페인", "멕시코", "스웨덴", "네덜란드", "터키",
        "뉴질랜드", "아르헨티나", "폴란드", "남아프리카 공화국"
    ]

    def select_country_sidebar(self):
        selected_country = st.sidebar.selectbox("국가 선택", self.COUNTRIES)
        with open(os.path.join("../data", "country_code.json"), "r") as f:
            country_codes = json.load(f)

        return country_codes[selected_country]

    def generate_wordcloud_button(self):
        return st.sidebar.button("워드클라우드 생성")

class RankingView:

    def split_dataframe(self, input_df, rows):
        return [input_df.loc[i:i+rows-1, :] for i in range(0, len(input_df), rows)]

    def display_ranking(self, ranking_df) -> None:
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
            batch_size = st.selectbox("총 페이지", options=[25, 50, 100])

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
        st.image(wordcloud, width=500, caption='인기 동영상 제목 워드클라우드')