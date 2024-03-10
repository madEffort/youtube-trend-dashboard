class InputModel:
    
    def __init__(self):
        self.selected_locale = ""
        self.question_text = ""
    
    def set_selected_country(self, country):
        self.selected_country = country
    
    def set_question_text(self, question):
        self.question_text = question
        
    def get_selected_country(self):
        return self.selected_country

    def get_question_text(self):
        return self.question_text
    

class PandasAIModel:
    def __init__(self):
        self.response_text = ""
    
    def set_response_text(self, response):
        self.response_text = response
    
    def get_response_text(self):
        return self.response_text

class RankingModel:
    def __init__(self):
        self.ranking_df = None
    
    def set_ranking_df(self, ranking_df):
        self.ranking_df = ranking_df
    
    def get_ranking_df(self):
        return self.ranking_df
    
