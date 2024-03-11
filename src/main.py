# main.py

from model import InputModel, RankingModel, AnalysisModel
from view import InputView, RankingView, AnalysisView
from controller import InputController, RankingController, AnalysisController

def main():

    input_model = InputModel()
    analysis_model = AnalysisModel()
    ranking_model = RankingModel()
    
    input_view = InputView()
    analysis_view = AnalysisView()
    ranking_view = RankingView()
    
    input_controller = InputController(input_model, input_view)
    analysis_controller = AnalysisController(analysis_model, analysis_view)
    ranking_controller = RankingController(ranking_model, ranking_view)

    input_controller.run()
    selected_country = input_model.get_selected_country()

    ranking_controller.load_ranking(selected_country)
    ranking_controller.display_ranking()
    
    selected_function = input_view.select_function_sidebar()
    if input_view.confirm_function_button():
        input_controller.handle_function(selected_function, ranking_model.get_ranking_df())
    
    if input_view.generate_wordcloud_button():
        analysis_controller.display_wordcloud(ranking_model.get_ranking_df())

if __name__ == '__main__':
    main()