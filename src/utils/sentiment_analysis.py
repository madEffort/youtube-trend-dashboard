from transformers import pipeline


class SentimentAnalyzer:

    def __init__(self):
        self.classifier = pipeline(
            "text-classification", model="matthewburke/korean_sentiment"
        )

    def analyze(self, comments):
        positive_comments = []
        negative_comments = []

        analysis = [0, 0]

        for comment in comments:
            # 한국어 감정 분석 모델을 사용하여 댓글의 감정 분석 수행
            preds = self.classifier(comment[0:512], return_all_scores=True)
            is_positive = preds[0][1]["score"] > 0.5
            if is_positive:
                analysis[0] += 1
                if len(positive_comments) < 5:
                    positive_comments.append(comment)
            else:
                analysis[1] += 1
                if len(negative_comments) < 5:
                    negative_comments.append(comment)
        return analysis, positive_comments, negative_comments
