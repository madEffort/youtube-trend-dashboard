# main.py
from model import InputModel, RankingModel
from view import InputView, RankingView
from controller import InputController, RankingController
import re

def main():

    input_model = InputModel()
    ranking_model = RankingModel()
    
    input_view = InputView()
    ranking_view = RankingView()
    
    input_controller = InputController(input_model, input_view)
    ranking_controller = RankingController(ranking_model, ranking_view)

    input_controller.run()
    selected_country = input_model.get_selected_country()

    ranking_controller.load_ranking(selected_country)
    ranking_controller.display_ranking()
    
    selected_function = input_view.select_function_sidebar()
    if input_view.confirm_function_button():
        input_controller.handle_function(selected_function, ranking_model.get_ranking_df())
    
    if input_view.generate_wordcloud_button():
        input_controller.display_wordcloud(ranking_model.get_ranking_df())

    input_video_id, analysis_btn = input_view.input_analysis_video()
    if analysis_btn:
        try:
            id_pattern = re.compile("[A-Za-z0-9_\-]{11}")
            video_id = id_pattern.search(input_video_id).group()
            if video_id is not None:
                ranking_controller.load_comments_analysis(video_id)
            else:
                input_view.input_analysis_invalid()
        except:
            input_view.input_analysis_invalid()
    

if __name__ == '__main__':
    main()
