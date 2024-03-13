# model.py


class InputModel:

    def __init__(self):
        self.selected_locale = ""

    def set_selected_country(self, country):
        self.selected_country = country

    def get_selected_country(self):
        return self.selected_country

    def set_selected_function(self, function):
        self.selected_function = function

    def get_selected_function(self):
        return self.selected_function


class RankingModel:
    def __init__(self):
        self.ranking_df = None

    def set_ranking_df(self, ranking_df):
        self.ranking_df = ranking_df

    def get_ranking_df(self):
        return self.ranking_df

