from enum import Enum

from .app import App
from .scene import Scene
from .widgets import WidgetBuilder
from .widgets.layer import Layer


class GameState(Enum):
    MENU = 0b000
    INGAME = 0b001
    PAUSE = 0b010
    SETTINGS = 0b100 | PAUSE


class Game(App):
    def __init__(self) -> None:
        scenes = {GameState.MENU: Scene([WidgetBuilder(Layer, outline=("Red", 5))])}
        state = GameState.MENU
        super().__init__(scenes, state)
