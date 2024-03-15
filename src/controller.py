import os
import json
import pandas as pd
from datetime import datetime
from dateutil import parser
from wordcloud import WordCloud
from decouple import config
from googleapiclient.discovery import build
from openai import OpenAI
from transformers import pipeline

# 요일 이름을 한국어로 매핑하는 딕셔너리
DAY_NAME_MAP = {
    "Monday": "월요일",
    "Tuesday": "화요일",
    "Wednesday": "수요일",
    "Thursday": "목요일",
    "Friday": "금요일",
    "Saturday": "토요일",
    "Sunday": "일요일",
}


class InputController:
    def __init__(self, input_model, input_view):
        # 입력 모델과 뷰를 초기화
        self.input_model = input_model
        self.input_view = input_view
        # OpenAI API 클라이언트 인스턴스 생성
        self.client = OpenAI(api_key=config("OPENAI_API_KEY"))

    def run(self):
        selected_country = self.input_view.select_country_sidebar()
        self.input_model.set_selected_country(selected_country)

    def display_wordcloud(self, ranking_df):
        # 데이터프레임에서 제목 열을 기반으로 워드클라우드 생성
        ranking_df["words"] = ranking_df["제목"].apply(
            lambda x: [item for item in str(x).split()]
        )
        all_words = list([a for b in ranking_df["words"].tolist() for a in b])
        all_words_str = " ".join(all_words)
        # OpenAI API를 사용하여 챗봇에게 인기있는 주제 추천 요청
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            top_p=0.1,
            temperature=0.1,
            messages=[
                {
                    "role": "system",
                    "content": "너는 인기 동영상 트렌드와 동영상 댓글을 분석을 도와주는 챗봇이야.",
                },
                {
                    "role": "user",
                    "content": f"이 데이터는 유튜브 인기동영상들의 제목들을 이어붙인 것인데 최근 인기있는 주제 또는 키워드가 무엇인지 이 데이터를 바탕으로 현재 가장 인기았는 구체적인 주제를 3가지 알려주고 조회수를 많이 받을 수 있는 구체적인 주제 2가지를 추천해줘 {all_words_str}",
                },
            ],
        )
        # 워드클라우드 생성
        wordcloud = WordCloud(
            font_path="AppleGothic", background_color="white", width=700, height=250
        ).generate(all_words_str)
        wordcloud_array = wordcloud.to_array()
        # 워드클라우드 및 챗봇 응답을 뷰에 표시
        self.input_view.display_wordcloud(
            wordcloud_array, response.choices[0].message.content
        )

    def handle_function(self, selected_function, ranking_df):
        # 선택된 기능에 따라 적절한 함수 호출
        if selected_function == "요일별 인기 동영상 업로드 비율":
            self.function_upload_status_by_weekday(ranking_df)
        elif selected_function == "시간대별 인기 동영상 업로드 비율":
            self.function_upload_status_by_time(ranking_df)
        elif selected_function == "인기 동영상 평균 태그 갯수":
            self.function_average_tags_count(ranking_df)

    def function_upload_status_by_weekday(self, ranking_df):
        # 요일별 업로드 현황을 계산하고 챗봇에게 문장 생성 요청
        weekday_data = {
            "A.월요일": ranking_df["업로드요일"].value_counts().get("월요일", 0),
            "B.화요일": ranking_df["업로드요일"].value_counts().get("화요일", 0),
            "C.수요일": ranking_df["업로드요일"].value_counts().get("수요일", 0),
            "D.목요일": ranking_df["업로드요일"].value_counts().get("목요일", 0),
            "E.금요일": ranking_df["업로드요일"].value_counts().get("금요일", 0),
            "F.토요일": ranking_df["업로드요일"].value_counts().get("토요일", 0),
            "G.일요일": ranking_df["업로드요일"].value_counts().get("일요일", 0),
        }
        weekday_df = pd.DataFrame([weekday_data])
        weekday_df = weekday_df.T
        weekday_df.columns = ["업로드 수"]
        # OpenAI API를 사용하여 챗봇에게 어느 요일에 업로드할지 추천 요청
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            top_p=0.1,
            temperature=0.1,
            messages=[
                {
                    "role": "system",
                    "content": "너는 인기 동영상 트렌드와 동영상 댓글을 분석을 도와주는 챗봇이야.",
                },
                {
                    "role": "user",
                    "content": f"이 데이터는 조회수가 급증한 유튜브 인기동영상들의 월요일부터 일요일까지 요일별로 업로드 수 현황인데 이 업로드 현황 데이터만을 바탕으로 어느 요일에 동영상을 업로드 하는게 조회수를 많이 받을 수 있는지 조언해줘. {weekday_df.to_string()}",
                },
            ],
        )
        # 결과를 뷰에 전달
        self.input_view.result_by_function(
            "요일별 인기 동영상 업로드 비율",
            (weekday_df, response.choices[0].message.content),
        )

    def function_upload_status_by_time(self, ranking_df):
        # 시간대별 업로드 현황을 계산하고 챗봇에게 문장 생성 요청
        ranking_df["업로드 시간"] = pd.to_datetime(ranking_df["업로드날짜"])
        upload_hours = ranking_df["업로드 시간"].dt.hour
        upload_hours_distribution = upload_hours.value_counts().sort_index()
        # OpenAI API를 사용하여 챗봇에게 어느 시간대에 업로드할지 추천 요청
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            top_p=0.1,
            temperature=0.1,
            messages=[
                {
                    "role": "system",
                    "content": "너는 인기 동영상 트렌드와 동영상 댓글을 분석을 도와주는 챗봇이야.",
                },
                {
                    "role": "user",
                    "content": f"이 데이터는 유튜브 인기동영상들의 0시부터 23시까지 시간대별로 업로드 수 분포현황인데 이 분포 현황을 바탕으로 어느 시간대에 동영상을 업로드 하는게 조회수를 많이 받을 수 있는지 조언해줘. {upload_hours_distribution.to_string()}",
                },
            ],
        )
        upload_hours_distribution.index = [
            int(hour) for hour in upload_hours_distribution.index
        ]
        # 결과를 뷰에 전달
        self.input_view.result_by_function(
            "시간대별 인기 동영상 업로드 비율",
            (upload_hours_distribution, response.choices[0].message.content),
        )

    def function_average_tags_count(self, ranking_df):
        # 태그 갯수의 평균을 계산하여 결과를 뷰에 전달
        average_tags = int(ranking_df["태그갯수"].mean())
        self.input_view.result_by_function("인기 동영상 평균 태그 갯수", average_tags)

    def compare_youtube_videos(
        self, ranking_df, video_id_1, video_id_2, ranking_controller
    ):
        select_video_1 = ranking_df[ranking_df["동영상ID"] == video_id_1]
        select_video_2 = ranking_df[ranking_df["동영상ID"] == video_id_2]
        print(select_video_1)
        print(select_video_2)
        videos = [
            self.preprocess_compare_video(select_video_1),
            self.preprocess_compare_video(select_video_2),
        ]
        video_1_result = ranking_controller.load_comments_analysis(video_id_1)
        video_2_result = ranking_controller.load_comments_analysis(video_id_2)
        comments_result1 = [
            video_1_result[1][0] * 2,
            video_1_result[1][1] * 2,
        ]  # 첫번째 비디오의 댓글 긍정 반응과 부정 반응 결과
        comments_result2 = [
            video_2_result[1][0] * 2,
            video_2_result[1][1] * 2,
        ]  # 두번째 비디오의 댓글 긍정 반응과 부정 반응 결과
        self.input_view.display_compare_results(
            videos, comments_result1, comments_result2
        )

    def preprocess_compare_video(self, video):
        return {
            "채널명": video["채널명"].iloc[0],
            "제목": video["제목"].iloc[0],
            "태그": video["태그"].iloc[0],
            "카테고리": video["카테고리"].iloc[0],
            "업로드날짜": datetime.fromisoformat(
                str(video["업로드날짜"].iloc[0])
            ).strftime("%Y. %m. %d."),
            "업로드요일": video["업로드요일"].iloc[0],
            "조회수": video["조회수"].iloc[0],
            "좋아요수": video["좋아요수"].iloc[0],
            "댓글수": video["댓글수"].iloc[0],
            "동영상링크": "https://www.youtube.com/watch?v={0}".format(
                video["동영상ID"].iloc[0]
            ),
        }


class RankingController:
    API_SERVICE_NAME = "youtube"
    API_VERSION = "v3"

    def __init__(self, ranking_model, ranking_view):
        self.youtube = build(
            self.API_SERVICE_NAME,
            self.API_VERSION,
            developerKey=config("YOUTUBE_API_KEY"),
        )
        self.ranking_model = ranking_model
        self.ranking_view = ranking_view
        # 한국어 감정 분석 모델을 초기화
        self.classifier = pipeline(
            "text-classification", model="matthewburke/korean_sentiment"
        )

    # 데이터 전처리 함수
    def preprocess_data(self, videos_df):
        numeric_cols = ["조회수", "좋아요수", "댓글수"]
        videos_df[numeric_cols] = videos_df[numeric_cols].apply(
            pd.to_numeric, errors="coerce", axis=1
        )
        videos_df["업로드날짜"] = videos_df["업로드날짜"].apply(
            lambda x: parser.parse(x)
        )
        videos_df["업로드요일"] = videos_df["업로드날짜"].apply(
            lambda x: x.strftime("%A")
        )
        videos_df["업로드요일"] = videos_df["업로드요일"].map(DAY_NAME_MAP)
        videos_df["태그갯수"] = videos_df["태그"].apply(
            lambda x: 0 if x is None else len(x)
        )
        videos_df["태그"] = videos_df["태그"].apply(
            lambda x: tuple(x) if isinstance(x, list) else x
        )
        return videos_df

    # 유튜브 API를 사용하여 인기 동영상 데이터를 로드
    def load_ranking(self, country="KR"):
        videos_data = []
        next_page_token = None
        while True:
            request = self.youtube.videos().list(
                part="snippet,contentDetails,statistics",
                chart="mostPopular",
                regionCode=country,
                maxResults=50,
                pageToken=next_page_token,
            )
            response = request.execute()
            for item in response["items"]:
                data = {
                    "채널명": item["snippet"].get("channelTitle", None),
                    "제목": item["snippet"].get("title", None),
                    "설명": item["snippet"].get("description", None),
                    "태그": item["snippet"].get("tags", []),
                    "카테고리": item["snippet"].get("categoryId", None),
                    "업로드날짜": item["snippet"].get("publishedAt", None),
                    "조회수": item["statistics"].get("viewCount", 0),
                    "좋아요수": item["statistics"].get("likeCount", 0),
                    "댓글수": item["statistics"].get("commentCount", 0),
                    "채널ID": item["snippet"].get("channelId", None),
                    "동영상ID": item.get("id", None),
                }
                videos_data.append(data)
            next_page_token = response.get("nextPageToken")
            if not next_page_token:
                break
        videos_df = self.preprocess_data(pd.DataFrame(videos_data))
        videos_df.to_csv(
            os.path.abspath(
                os.path.join(os.path.dirname(__file__), "..", "data", "dataframe.csv")
            )
        )
        with open(
            os.path.abspath(
                os.path.join(
                    os.path.dirname(__file__), "..", "data", "category_code.json"
                )
            ),
            "r",
        ) as f:
            category_mapping = json.load(f)
        videos_df["카테고리"] = videos_df["카테고리"].map(category_mapping)
        videos_df["랭킹"] = range(0, len(videos_df))
        videos_df = videos_df.set_index("랭킹")
        self.ranking_model.set_ranking_df(videos_df)

    def display_ranking(self):
        # 랭킹 데이터를 뷰에 전달하여 표시
        ranking_df = self.ranking_model.get_ranking_df()
        self.ranking_view.display_ranking(ranking_df)

    def load_comments_analysis(self, video_id):
        # 동영상 댓글을 분석하여 긍정적인 댓글과 부정적인 댓글 수 계산
        request = self.youtube.commentThreads().list(
            part="id, replies, snippet", videoId=video_id, maxResults=50
        )
        response = request.execute()
        comments = [
            item["snippet"]["topLevelComment"]["snippet"]["textOriginal"]
            for item in response["items"]
        ]
        analysis = [0, 0]
        for comment in comments:
            if self.sentiment_analysis(comment) == "positive":
                analysis[0] += 1
            elif self.sentiment_analysis(comment) == "negative":
                analysis[1] += 1
        return (video_id, analysis)

    def sentiment_analysis(self, comment):
        # 한국어 감정 분석 모델을 사용하여 댓글의 감정 분석 수행
        preds = self.classifier(comment[0:512], return_all_scores=True)
        is_positive = preds[0][1]["score"] > 0.5
        if is_positive:
            return "positive"
        else:
            return "negative"
