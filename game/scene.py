from typing import List, Optional

import pygame
from pygame import Surface
from pygame.event import Event

from .types import ColorValue, KeyCode, KeyHandler
from .widgets import WidgetBuilder
from .widgets.layer import LayerWidget


class Scene:
    layers: List[WidgetBuilder[LayerWidget]]
    screen: Optional[Surface]
    _layers: List[LayerWidget]
    shortcuts: dict[KeyCode, KeyHandler]

    def __init__(
        self,
        layers: Optional[list[WidgetBuilder]] = None,
        shortcuts=None,
        background: ColorValue = "White",
    ) -> None:
        self.background = background
        if layers:
            self.layers = layers
        else:
            self.layers = []
        self._layers = []
        if shortcuts:
            self.shortcuts = shortcuts
        else:
            self.shortcuts = {}

    def set_screen(self, screen: Surface):
        self.screen = screen
        rect = screen.get_rect()
        self._layers = [layer.build(rect) for layer in self.layers]

    def handle_event(self, event: Event):
        match event.type:
            case pygame.KEYDOWN | pygame.KEYUP:
                shortcut = self.shortcuts.get(event.key)
                if shortcut:
                    shortcut(event.type)
            case pygame.MOUSEMOTION:
                for widget in self._layers:
                    widget.focus(event.pos)

    def draw(self):
        if not self.screen:
            return
        self.screen.fill(self.background)
        for widget in self._layers:
            widget.draw(self.screen)
