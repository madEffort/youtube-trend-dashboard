from model import InputModel, RankingModel, AnalysisModel
from view import InputView, RankingView, AnalysisView
from controller import InputController, RankingController, AnalysisController

def main():

    input_model = InputModel()
    input_view = InputView()
    input_controller = InputController(input_model, input_view)
    
    ranking_model = RankingModel()
    ranking_view = RankingView()
    ranking_controller = RankingController(ranking_model, ranking_view)
    
    analysis_model = AnalysisModel()
    analysis_view = AnalysisView()
    analysis_controller = AnalysisController(analysis_model, analysis_view)

    input_controller.run()
    selected_country = input_model.get_selected_country()

    ranking_controller.load_ranking(selected_country)
    ranking_controller.display_ranking()

    if input_view.generate_wordcloud_button():
        analysis_controller.display_wordcloud(ranking_model.get_ranking_df())

if __name__ == '__main__':
    main()