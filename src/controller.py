import json
import pandas as pd
from googleapiclient.discovery import build
from decouple import config
from dateutil import parser
from wordcloud import WordCloud

class InputController:

    def __init__(self, input_model, input_view):
        self.input_model = input_model
        self.input_view = input_view

    def run(self):
        selected_country = self.input_view.select_country_sidebar()
        self.input_model.set_selected_country(selected_country)


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

    def preprocess_data(self, videos_df):
        numeric_cols = ["viewCount", "likeCount", "commentCount"]
        videos_df[numeric_cols] = videos_df[numeric_cols].apply(
            pd.to_numeric, errors="coerce", axis=1
        )
        videos_df["publishedAt"] = videos_df["publishedAt"].apply(
            lambda x: parser.parse(x)
        )
        videos_df["publishDayName"] = videos_df["publishedAt"].apply(
            lambda x: x.strftime("%A")
        )
        videos_df["tagCount"] = videos_df["tags"].apply(
            lambda x: 0 if x is None else len(x)
        )
        videos_df["tags"] = videos_df["tags"].apply(
            lambda x: tuple(x) if isinstance(x, list) else x
        )
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
                    "channelId": item["snippet"].get("channelId", None),
                    "channelName": item["snippet"].get("channelTitle", None),
                    "videoId": item.get("id", None),
                    "title": item["snippet"].get("title", None),
                    "thumbnails": item["snippet"]["thumbnails"]["default"].get(
                        "url", None
                    ),
                    "publishedAt": item["snippet"].get("publishedAt", None),
                    "description": item["snippet"].get("description", None),
                    "tags": item["snippet"].get("tags", []),
                    "categoryId": item["snippet"].get("categoryId", None),
                    "viewCount": item["statistics"].get("viewCount", 0),
                    "likeCount": item["statistics"].get("likeCount", 0),
                    "commentCount": item["statistics"].get("commentCount", 0),
                }
                videos_data.append(data)
            next_page_token = response.get("nextPageToken")
            if not next_page_token:
                break

        videos_df = self.preprocess_data(pd.DataFrame(videos_data))

        with open("../data/category_code.json", "r") as f:
            category_mapping = json.load(f)

        videos_df["categoryId"] = videos_df["categoryId"].map(category_mapping)

        videos_df["ranking"] = range(0, len(videos_df))
        videos_df = videos_df.set_index("ranking")

        self.ranking_model.set_ranking_df(videos_df)

    def display_ranking(self):
        ranking_df = self.ranking_model.get_ranking_df()
        self.ranking_view.display_ranking(ranking_df)


class AnalysisController:

    def __init__(self, analysis_model, analysis_view):
        self.analysis_model = analysis_model
        self.analysis_view = analysis_view

    def display_wordcloud(self, ranking_df):
        ranking_df["title_words"] = ranking_df["title"].apply(
            lambda x: [item for item in str(x).split()]
        )
        all_words = list([a for b in ranking_df["title_words"].tolist() for a in b])
        all_words_str = " ".join(all_words)

        wordcloud = WordCloud(
            font_path="AppleGothic", background_color="white"
        ).generate(all_words_str)
        wordcloud_array = wordcloud.to_array()
        self.analysis_view.display_wordcloud(wordcloud_array)