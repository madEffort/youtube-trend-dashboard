import streamlit as st


class InputView:

    def sidebar_select_country(self):
        selected_country = st.sidebar.selectbox("국가 선택", ["USA", "UK", "Canada"])
        return selected_country

    def question_text_area(self):
        question_text = st.sidebar.text_area("질문을 입력하세요.")
        return question_text

    def submit_button(self):
        return st.sidebar.button("질문하기")


class PandasAIView:

    def display_response(self, response):
        st.write(response)


class RankingView:

    def display_ranking(self, ranking_df):
        st.dataframe(ranking_df)
