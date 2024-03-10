from model import InputModel, PandasAIModel, RankingModel
from view import InputView, PandasAIView, RankingView
from controller import InputController
def main():
    input_model = InputModel()
    input_view = InputView()
    input_controller = InputController(input_model, input_view)
    
    input_controller.run()
    
if __name__ == '__main__':
    main()