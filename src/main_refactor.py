from model_refactor import YoutubeModel
from view_refactor import display_sidebar
from controller_refactor import YoutubeController

if __name__ == "__main__":
    model = YoutubeModel()
    controller = YoutubeController(model)
    display_sidebar(controller)