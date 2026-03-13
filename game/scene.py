from typing import Dict, Optional, Tuple

import pygame
from pygame import Surface
from pygame.event import Event

from .types import ColorValue, KeyCode
from .widgets import WidgetBuilder
from .widgets.layer import LayerWidget


class Scene:
    layers: Tuple[WidgetBuilder[LayerWidget], ...]
    screen: Optional[Surface]
    _layers: Tuple[LayerWidget, ...]
    shortcuts: Dict[KeyCode, int]

    def __init__(
        self,
        layers: Optional[Tuple[WidgetBuilder[LayerWidget], ...]] = None,
        shortcuts: Optional[Dict[KeyCode, int]] = None,
        background: ColorValue = "White",
    ) -> None:
        self.background = background
        if layers:
            self.layers = layers
        else:
            self.layers = tuple()
        self._layers = tuple()
        if shortcuts:
            self.shortcuts = shortcuts
        else:
            self.shortcuts = {}

    def set_screen(self, screen: Surface):
        self.screen = screen
        rect = screen.get_rect()
        self._layers = tuple(layer.build(rect) for layer in self.layers)

    def handle_event(self, event: Event) -> bool:
        match event.type:
            case pygame.KEYDOWN | pygame.KEYUP:
                event_type = self.shortcuts.get(event.key)
                if event_type:
                    pygame.event.post(pygame.event.Event(event_type))
                return event_type is not None
        for layer in reversed(self._layers):
            if layer.handle_event(event):
                return True
        return False

    def draw(self):
        if not self.screen:
            return
        self.screen.fill(self.background)
        for widget in self._layers:
            widget.draw(self.screen)
