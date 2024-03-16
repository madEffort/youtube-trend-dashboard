from analysis_options import ANALYSIS_OPTIONS
from controller_chart import (
    generate_dayofweek_chart,
    generate_timebyday_chart,
    generate_pie_chart,
)
import os
import re
import pandas as pd
from datetime import datetime
from wordcloud import WordCloud
from decouple import config
from openai import OpenAI
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
from sentiment_analysis import SentimentAnalyzer


class YoutubeController:

    API_SERVICE_NAME = "youtube"
    API_VERSION = "v3"

    def __init__(self, model):
        self.model = model
        self.client = OpenAI(api_key=config("OPENAI_API_KEY"))
        self.youtube = build(
            self.API_SERVICE_NAME,
            self.API_VERSION,
            developerKey=config("YOUTUBE_API_KEY"),
        )

    def get_popular_videos_data(self, country_code):
        # 국가 선택에 따른 인기 동영상 데이터 요청
        self.model.fetch_popular_videos_data(country_code)

        return self.model.get_youtube_dataframe()

    def analyze_youtube_by_option(self, analysis_option):
        if analysis_option == ANALYSIS_OPTIONS[0]:

            youtube_dataframe = self.model.get_youtube_dataframe()

            weekday_data = {
                "월요일": youtube_dataframe["업로드요일"]
                .value_counts()
                .get("월요일", 0),
                "화요일": youtube_dataframe["업로드요일"]
                .value_counts()
                .get("화요일", 0),
                "수요일": youtube_dataframe["업로드요일"]
                .value_counts()
                .get("수요일", 0),
                "목요일": youtube_dataframe["업로드요일"]
                .value_counts()
                .get("목요일", 0),
                "금요일": youtube_dataframe["업로드요일"]
                .value_counts()
                .get("금요일", 0),
                "토요일": youtube_dataframe["업로드요일"]
                .value_counts()
                .get("토요일", 0),
                "일요일": youtube_dataframe["업로드요일"]
                .value_counts()
                .get("일요일", 0),
            }
            result = pd.DataFrame([weekday_data])
            result = result.T
            result.columns = ["업로드 수"]

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
                        "content": f"이 데이터는 조회수가 급증한 유튜브 인기동영상들의 월요일부터 일요일까지 요일별로 업로드 수 현황인데 이 업로드 현황 데이터만을 바탕으로 어느 요일에 동영상을 업로드 하는게 조회수를 많이 받을 수 있는지 조언해줘. {result.to_string()}",
                    },
                ],
            )

            gpt_message = response.choices[0].message.content
            result = generate_dayofweek_chart(result)

            return analysis_option, (result, gpt_message)

        if analysis_option == ANALYSIS_OPTIONS[1]:
            print("시간별")

            youtube_dataframe = self.model.get_youtube_dataframe()

            youtube_dataframe["업로드 시간"] = pd.to_datetime(
                youtube_dataframe["업로드날짜"]
            )
            upload_hours = youtube_dataframe["업로드 시간"].dt.hour
            result = upload_hours.value_counts().sort_index()

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
                        "content": f"이 데이터는 유튜브 인기동영상들의 0시부터 23시까지 시간대별로 업로드 수 분포현황인데 이 분포 현황을 바탕으로 어느 시간대에 동영상을 업로드 하는게 조회수를 많이 받을 수 있는지 조언해줘. {result.to_string()}",
                    },
                ],
            )
            result.index = [int(hour) for hour in result.index]

            gpt_message = response.choices[0].message.content
            result = generate_timebyday_chart(result)

            return analysis_option, (result, gpt_message)

        if analysis_option == ANALYSIS_OPTIONS[2]:
            print("asd")
            youtube_dataframe = self.model.get_youtube_dataframe()

            result = int(youtube_dataframe["태그갯수"].mean())
            return analysis_option, result

    def generate_wordcloud(self):
        youtube_dataframe = self.model.get_youtube_dataframe()

        youtube_dataframe["words"] = youtube_dataframe["제목"].apply(
            lambda x: [item for item in str(x).split()]
        )
        all_words = list([a for b in youtube_dataframe["words"].tolist() for a in b])
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
            font_path="AppleGothic", background_color="white", width=700, height=300
        ).generate(all_words_str)

        gpt_message = response.choices[0].message.content
        result = wordcloud.to_array()

        return result, gpt_message

    def analyze_comments(self, video_id):
        # 동영상 댓글 분석 요청

        request = self.youtube.commentThreads().list(
            part="id, replies, snippet", videoId=video_id, maxResults=50
        )
        response = request.execute()
        comments = [
            item["snippet"]["topLevelComment"]["snippet"]["textOriginal"]
            for item in response["items"]
        ]

        sentiment_analyzer = SentimentAnalyzer()

        result, positive_comments, negative_comments = sentiment_analyzer.analyze(
            comments
        )

        return result, positive_comments, negative_comments, video_id

    def analyze_slang_beta(self, video_id):
        warning = 0
        srt = YouTubeTranscriptApi.get_transcript(video_id, languages=["ko", "en"])

        with open(
            os.path.abspath(
                os.path.join(os.path.dirname(__file__), "..", "data", "slang.txt")
            ),
            "r",
            encoding="utf-8",
        ) as f:
            lines = f.read().splitlines()

        slang = set(lines)

        with open(
            os.path.abspath(
                os.path.join(os.path.dirname(__file__), "..", "data", "subtitle.txt")
            ),
            "w",
            encoding="utf-8",
        ) as f:
            for data in srt:
                f.write(f"{data['text']}\n")

        with open(
            os.path.abspath(
                os.path.join(os.path.dirname(__file__), "..", "data", "subtitle.txt")
            ),
            "r",
            encoding="utf-8",
        ) as f:
            pattern = "|".join(slang)
            for data in f.readlines():
                if re.search(pattern, data, re.IGNORECASE):
                    warning += 1

        return warning

    def compare_youtube_videos(self, video_id_1, video_id_2):

        youtube_dataframe = self.model.get_youtube_dataframe()

        select_video_1 = youtube_dataframe[youtube_dataframe["동영상ID"] == video_id_1]
        select_video_2 = youtube_dataframe[youtube_dataframe["동영상ID"] == video_id_2]

        def preprocess_compare_video(video):
            return {
                "채널명": video["채널명"].iloc[0],
                "제목": video["제목"].iloc[0],
                "태그": (
                    video["태그"].iloc[0]
                    if len(video["태그"].iloc[0])
                    else "사용한 태그가 없습니다."
                ),
                "카테고리": video["카테고리"].iloc[0],
                "업로드날짜": datetime.fromisoformat(
                    str(video["업로드날짜"].iloc[0])
                ).strftime("%Y. %m. %d."),
                "업로드요일": video["업로드요일"].iloc[0],
                "조회수": video["조회수"].iloc[0],
                "좋아요 수": video["좋아요수"].iloc[0],
                "댓글 수": video["댓글수"].iloc[0],
                "동영상링크": "https://www.youtube.com/watch?v={0}".format(
                    video["동영상ID"].iloc[0]
                ),
            }

        videos = [
            preprocess_compare_video(select_video_1),
            preprocess_compare_video(select_video_2),
        ]

        video1_result, video1_positive_comments, video1_negative_comments, _ = (
            self.analyze_comments(video_id_1)
        )
        video2_result, video2_positive_comments, video2_negative_comments, _ = (
            self.analyze_comments(video_id_2)
        )

        comments_result1 = [
            video1_result[0] * 2,
            video1_result[1] * 2,
        ]  # 첫번째 비디오의 댓글 긍정 반응과 부정 반응 결과
        comments_result2 = [
            video2_result[0] * 2,
            video2_result[1] * 2,
        ]  # 두번째 비디오의 댓글 긍정 반응과 부정 반응 결과

        comments_pie_chart = generate_pie_chart(videos, option="댓글 수")
        likes_pie_chart = generate_pie_chart(videos, option="좋아요 수")

        return (
            videos,
            (comments_result1, [video1_positive_comments, video1_negative_comments]),
            (comments_result2, [video2_positive_comments, video2_negative_comments]),
            comments_pie_chart,
            likes_pie_chart,
        )
