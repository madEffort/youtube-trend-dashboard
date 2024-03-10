from model import InputModel, PandasAIModel, RankingModel
from view import InputView, PandasAIView, RankingView
import pandas as pd

class InputController:
    
    def __init__(self, input_model, input_view):
        self.input_model = input_model
        self.input_view = input_view
        
    def run(self):
        selected_country = self.input_view.sidebar_select_country()
        self.input_model.set_selected_country(selected_country)
        
        question_text = self.input_view.question_text_area()
        self.input_model.set_question_text(question_text)
        
        if self.input_view.submit_button():
            selected_country = self.input_model.get_selected_country()
            question_text = self.input_model.get_question_text()
            
            print(selected_country)
            print(question_text)
