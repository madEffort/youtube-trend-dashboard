from page_config import init_setting
from model_refactor import YoutubeModel
from view_refactor import display_sidebar
from controller_refactor import YoutubeController

init_setting()

def main():
    model = YoutubeModel()
    controller = YoutubeController(model)
    display_sidebar(controller)

if __name__ == "__main__":
    main()