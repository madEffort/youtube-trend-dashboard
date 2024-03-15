class InputModel:
    def __init__(self):
        # 선택된 국가를 빈 문자열로 초기화합니다.
        self.selected_country = ""

    def set_selected_country(self, country):
        # 선택된 국가를 설정합니다.
        self.selected_country = country

    def get_selected_country(self):
        # 현재 선택된 국가를 반환합니다.
        return self.selected_country

    def set_selected_function(self, function):
        # 선택된 기능을 설정합니다.
        self.selected_function = function

    def get_selected_function(self):
        # 현재 선택된 기능을 반환합니다.
        return self.selected_function


class RankingModel:
    def __init__(self):
        # 순위 데이터프레임을 None으로 초기화합니다.
        self.ranking_df = None

    def set_ranking_df(self, ranking_df):
        # 순위 데이터프레임을 설정합니다.
        self.ranking_df = ranking_df

    def get_ranking_df(self):
        # 현재 설정된 순위 데이터프레임을 반환합니다.
        return self.ranking_df