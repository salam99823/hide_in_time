from typing import List, Optional

import pygame
from pygame import Surface
from pygame.event import Event

from game.widgets.layer import Layer

from .types import ColorValue, KeyCode, KeyHandler
from .widgets import WidgetBuilder


class Scene:
    layers: List[WidgetBuilder[Layer]]
    _layers: List[Layer]
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

    def handle_event(self, event: Event):
        match event.type:
            case pygame.KEYDOWN | pygame.KEYUP:
                shortcut = self.shortcuts.get(event.key)
                if shortcut:
                    shortcut(event.type)
            case pygame.MOUSEMOTION:
                for widget in self._layers:
                    widget.focus(event.pos)

    def draw(self, screen: Surface):
        screen.fill(self.background)
        screen_rect = screen.get_rect()
        self._layers.clear()
        for widget in self.layers:
            widget = widget.build(screen_rect)
            self._layers.append(widget)
            widget.draw(screen)
