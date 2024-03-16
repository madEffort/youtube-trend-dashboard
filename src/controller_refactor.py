class YoutubeController:
    def __init__(self, model):
        self.model = model

    def get_popular_videos_data(self, country_code):
        # 국가 선택에 따른 인기 동영상 데이터 요청
        return self.model.fetch_popular_videos_data(country_code)

    def analyze_comments(self, video_id):
        # 동영상 댓글 분석 요청
        return self.model.analyze_video_comments(video_id)

    def compare_videos(self, video_id_a, video_id_b):
        # 두 동영상 비교 분석 요청
        return self.model.compare_videos(video_id_a, video_id_b)