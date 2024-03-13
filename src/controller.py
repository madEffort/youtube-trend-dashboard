# controller.py
import os
from textblob import TextBlob
import json
import pandas as pd
from googleapiclient.discovery import build
from decouple import config
from dateutil import parser
from wordcloud import WordCloud

WEEKDAY = {
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
        self.input_model = input_model
        self.input_view = input_view

    def run(self):
        selected_country = self.input_view.select_country_sidebar()
        self.input_model.set_selected_country(selected_country)
        
    def display_wordcloud(self, ranking_df):

        ranking_df["words"] = ranking_df["제목"].apply(
            lambda x: [item for item in str(x).split()]
        )

        all_words = list([a for b in ranking_df["words"].tolist() for a in b])
        all_words_str = " ".join(all_words)

        wordcloud = WordCloud(
            font_path="AppleGothic", background_color="white", width=700, height=250
        ).generate(all_words_str)

        wordcloud_array = wordcloud.to_array()
        self.input_view.display_wordcloud(wordcloud_array)

    def handle_function(self, selected_function, ranking_df):
        if selected_function == "요일별 인기 동영상 업로드 비율":
            self.function_upload_status_by_weekday(ranking_df)
        elif selected_function == "시간대별 인기 동영상 업로드 비율":
            self.function_upload_status_by_time(ranking_df)
        elif selected_function == "인기 동영상 평균 태그 갯수":
            self.function_average_tags_count(ranking_df)

    def function_upload_status_by_weekday(self, ranking_df):
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
        self.input_view.result_by_function("요일별 인기 동영상 업로드 비율", weekday_df)

    def function_upload_status_by_time(self, ranking_df):
        ranking_df["업로드 시간"] = pd.to_datetime(ranking_df["업로드날짜"])
        upload_hours = ranking_df["업로드 시간"].dt.hour
        upload_hours_distribution = upload_hours.value_counts().sort_index()
        upload_hours_distribution.index = [
            int(hour) for hour in upload_hours_distribution.index
        ]
        self.input_view.result_by_function(
            "시간대별 인기 동영상 업로드 비율", upload_hours_distribution
        )

    def function_average_tags_count(self, ranking_df):
        average_tags = int(ranking_df['태그갯수'].mean())
        self.input_view.result_by_function("인기 동영상 평균 태그 갯수", average_tags)


class RankingController:

    API_SERVICE_NAME = "youtube"
    API_VERSION = "v3"
    # SCOPES = ['']

    def __init__(self, ranking_model, ranking_view):
        
        # credentials = None
        
        # if os.path.exists('../secrets/token.pickle'):
        #     with open('../secrets/token.pickle', 'rb') as token:
        #         credentials = pickle.load(token)
        
        # if not credentials or not credentials.valid:
        #     if credentials and credentials.expired and credentials.refresh_token:
        #         credentials.refresh(Request())
        #     else:
        #         flow = InstalledAppFlow.from_client_secrets_file("../secrets/token.json", scopes=self.SCOPES)
        #         flow.run_local_server(port=8080, prompt="consent", authorization_prompt_message="")
        #         credentials = flow.credentials

        #         with open("../secrets/token.pickle", "wb") as token:
        #             pickle.dump(credentials, token)
        
        self.youtube = build(
            self.API_SERVICE_NAME,
            self.API_VERSION,
            # credentials=credentials,
            developerKey=config('YOUTUBE_API_KEY')
        )
        self.ranking_model = ranking_model
        self.ranking_view = ranking_view

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
        videos_df["업로드요일"] = videos_df["업로드요일"].map(WEEKDAY)
        videos_df["태그갯수"] = videos_df["태그"].apply(
            lambda x: 0 if x is None else len(x)
        )
        videos_df["태그"] = videos_df["태그"].apply(
            lambda x: tuple(x) if isinstance(x, list) else x
        )
        
        videos_df = videos_df[
            [
                "채널명",
                "제목",
                "설명",
                "태그",
                "태그갯수",
                "카테고리",
                "조회수",
                "좋아요수",
                "댓글수",
                "업로드날짜",
                '업로드요일',
                "채널ID",
                "동영상ID",
            ]
        ]
        
        videos_df.to_html()
        
        return videos_df

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


        with open(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'category_code.json')), "r") as f:
            category_mapping = json.load(f)

        videos_df["카테고리"] = videos_df["카테고리"].map(category_mapping)

        videos_df["랭킹"] = range(0, len(videos_df))
        videos_df = videos_df.set_index("랭킹")

        self.ranking_model.set_ranking_df(videos_df)

    def display_ranking(self):
        ranking_df = self.ranking_model.get_ranking_df()
        self.ranking_view.display_ranking(ranking_df)

    def load_comments_analysis(self, video_id):
        # print(type(ranking_df))
        # print(ranking_num)
        # print(ranking_df.columns)
        # print(ranking_df[ranking_df['랭킹'] == str(ranking_num)])
        request = self.youtube.commentThreads().list(
            part='id, replies, snippet',
            videoId=video_id,
            maxResults=100
        )

        response = request.execute()
        
        comments = [item['snippet']['topLevelComment']['snippet']['textOriginal'] for item in response['items']]
        
        analysis = [0,0,0]
        for comment in comments:
            if self.sentiment_analysis(comment) == 'positive':
                analysis[0] += 1
            elif self.sentiment_analysis(comment) == 'netural':
                analysis[1] += 1
            elif self.sentiment_analysis(comment) == 'negative':
                analysis[2] += 1
        
        self.ranking_view.video_comments_analysis(video_id, analysis)
        print(analysis)
        
    def sentiment_analysis(self, comment):
        
        analysis = TextBlob(comment)
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'netural'
        else:
            return 'negative'
        
            