import os
import json
import pandas as pd
from dateutil import parser
from decouple import config
from googleapiclient.discovery import build

DAY_NAME_MAP = {
    "Monday": "월요일",
    "Tuesday": "화요일",
    "Wednesday": "수요일",
    "Thursday": "목요일",
    "Friday": "금요일",
    "Saturday": "토요일",
    "Sunday": "일요일",
}

class YoutubeModel:
    
    API_SERVICE_NAME = "youtube"
    API_VERSION = "v3"
    
    def __init__(self):
        self.youtube = build(
            self.API_SERVICE_NAME,
            self.API_VERSION,
            developerKey=config("YOUTUBE_API_KEY"),
        )

    def fetch_popular_videos_data(self, country_code):
        # 국가 코드에 따라 유튜브에서 인기 동영상 데이터를 가져오는 로직 구현
        videos_data = []
        next_page_token = None
        while True:
            request = self.youtube.videos().list(
                part="snippet,contentDetails,statistics",
                chart="mostPopular",
                regionCode=country_code,
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
        videos_df = pd.DataFrame(videos_data)
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
        return videos_df

    def analyze_video_comments(self, video_id):
        # 동영상 ID에 따라 댓글을 분석하는 로직 구현
        pass

    def compare_videos(self, video_id_a, video_id_b):
        # 두 동영상을 비교하는 로직 구현
        pass