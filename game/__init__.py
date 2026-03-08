from enum import Enum

from pygame import Rect

from game.widgets.text import Text

from .app import App
from .scene import Scene
from .widgets import Align, El, Widget
from .widgets.box import HBox, VBox
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
                (
                    Layer(
                        (
                            HBox(
                                Rect(0, 0, 1000, 100),
                                maximize=(True, False),
                                align_items=Align.TOP,
                                childs=(
                                    El(
                                        Widget,
                                        maximize=(True, False),
                                        background="Red",
                                    ),
                                    El(
                                        Widget,
                                        Rect(0, 0, 100, 100),
                                        background="Green",
                                    ),
                                    El(
                                        Widget,
                                        maximize=(True, False),
                                        background="Blue",
                                    ),
                                ),
                            ),
                            VBox(
                                maximize=(True, True),
                                childs=(
                                    El(
                                        Widget,
                                        Rect(0, 0, 100, 100),
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
                                ),
                            ),
                            HBox(
                                Rect(0, 0, 1000, 200),
                                maximize=(True, False),
                                # align_items=Align.BOTTOM,
                                childs=(
                                    El(
                                        Widget,
                                        Rect(0, 0, 100, 100),
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
                                ),
                            ),
                        ),
                        align_items=Align.BOTTOM,
                        outline=("Red", 5),
                    ),
                )
            )
        }
        state = GameState.MENU
        super().__init__(scenes, state)
