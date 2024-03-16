from config.page_config import set_page_config
from models.model import YoutubeModel
from views.view import display_sidebar
from controllers.controller import YoutubeController


def main():
    set_page_config()
    model = YoutubeModel()
    controller = YoutubeController(model)
    display_sidebar(controller)


if __name__ == "__main__":
    main()
