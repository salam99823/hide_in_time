from enum import Enum

import pygame
from pygame import QUIT, Rect
from pygame.event import Event

from .app import App
from .scene import Scene
from .widgets import button
from .widgets.box import VBox
from .widgets.button import Button
from .widgets.layer import Layer


class GameState(Enum):
    MENU = 0b000
    INGAME = 0b001
    PAUSE = 0b010
    SETTINGS = 0b100 | PAUSE


class MenuButton(Enum):
    PLAY_BUTTON = 0
    SETTINGS_BUTTON = 1
    EXIT_BUTTON = 2


class Game(App):
    def __init__(self) -> None:
        scenes = {
            GameState.MENU: Scene(
                (
                    Layer(
                        (
                            VBox(
                                maximize=(True, True),
                                childs=(
                                    Button(
                                        "Play",
                                        MenuButton.PLAY_BUTTON,
                                        Rect(0, 0, 300, 100),
                                        border=("Red", 3),
                                    ),
                                    Button(
                                        "Settings",
                                        MenuButton.SETTINGS_BUTTON,
                                        Rect(0, 0, 300, 100),
                                        border=("Red", 3),
                                    ),
                                    Button(
                                        "Exit",
                                        MenuButton.EXIT_BUTTON,
                                        Rect(0, 0, 200, 100),
                                        border=("Red", 3),
                                    ),
                                ),
                            ),
                        ),
                    ),
                ),
            ),
            GameState.INGAME: Scene(
                (
                    # Layer(
                    # ),
                )
            ),
        }
        state = GameState.MENU
        super().__init__(scenes, state)

    def run(self):
        for event in super().run():
            match event.type:
                case button.BUTTONUP:
                    match event.button_id:
                        case MenuButton.PLAY_BUTTON:
                            self.state = GameState.INGAME
                            scene = self.scenes[self.state]
                            scene.set_screen(self.screen)
                        case MenuButton.EXIT_BUTTON:
                            pygame.event.post(Event(QUIT))
                case _:
                    yield event
