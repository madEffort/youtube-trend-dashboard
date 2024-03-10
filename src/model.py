
class InputModel:
    
    def __init__(self):
        self.selected_locale = ""

    def set_selected_country(self, country):
        self.selected_country = country
    
    def get_selected_country(self):
        return self.selected_country

class RankingModel:
    def __init__(self):
        self.ranking_df = None
        self.current_df = None
        
    def set_ranking_df(self, ranking_df):
        self.ranking_df = ranking_df
    
    def get_ranking_df(self):
        return self.ranking_df
    
    def set_current_df(self, current_df):
        self.current_df = current_df
    
    def get_current_df(self):
        return self.current_df

class AnalysisModel:
    
    def __init__(self):
        self.ranking_df = None
        
    def set_ranking_df(self, ranking_df):
        self.ranking_df = ranking_df
    
    def get_ranking_df(self):
        return self.ranking_df
