from enum import Enum

from pygame import Rect

from .app import App
from .scene import Scene
from .widgets import Align, El, Widget
from .widgets.box import VBox
from .widgets.layer import Layer


class GameState(Enum):
    MENU = 0b000
    INGAME = 0b001
    PAUSE = 0b010
    SETTINGS = 0b100 | PAUSE


class Game(App):
    def __init__(self) -> None:
        scenes = {
            GameState.MENU: Scene(
                [
                    Layer(
                        [
                            VBox(
                                Rect(0, 0, 300, 300),
                                align=Align.TOP,
                                childs=[
                                    El(
                                        Widget,
                                        rect=Rect(0, 0, 100, 100),
                                        background="Red",
                                    ),
                                    El(
                                        Widget,
                                        Rect(0, 0, 100, 100),
                                        background="Green",
                                    ),
                                    El(
                                        Widget,
                                        Rect(0, 0, 100, 100),
                                        background="Blue",
                                    ),
                                ],
                            )
                        ],
                        outline=("Red", 5),
                    )
                ]
            )
        }
        state = GameState.MENU
        super().__init__(scenes, state)
