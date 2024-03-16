from page_config import set_page_config
from model_refactor import YoutubeModel
from view_refactor import display_sidebar
from controller_refactor import YoutubeController

def main():
    set_page_config()
    model = YoutubeModel()
    controller = YoutubeController(model)
    display_sidebar(controller)

if __name__ == "__main__":
    main()