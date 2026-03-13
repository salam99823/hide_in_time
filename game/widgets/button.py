from enum import Enum
from typing import Optional

import pygame
from pygame import Surface
from pygame.event import Event

from .. import utils
from . import ColorValue, WidgetBuilder
from .label import LabelWidget

BUTTONDOWN = utils.new_event_type()
BUTTONUP = utils.new_event_type()


def Button(text: str, id: Enum, *args, **kwargs) -> WidgetBuilder["ButtonWidget"]:
    return WidgetBuilder(ButtonWidget, *args, text=text, id=id, **kwargs)


class ButtonWidget(LabelWidget):
    id: Enum
    _normal_bg: Optional[ColorValue]
    _hover_bg: Optional[ColorValue]
    _active_bg: Optional[ColorValue]
    is_pressed: bool = False

    def __init__(
        self,
        text: str,
        id: Enum,
        hover_background: Optional[ColorValue] = (100, 100, 100),
        active_background: Optional[ColorValue] = (150, 150, 150),
        **kwargs,
    ) -> None:
        self.id = id
        self._normal_bg = kwargs.get("background")
        self._hover_bg = hover_background
        self._active_bg = active_background
        super().__init__(text=text, **kwargs)

    def handle_event(self, event: Event) -> bool:
        super().handle_event(event)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.howered:
                self.is_pressed = True
                pygame.event.post(
                    Event(
                        BUTTONDOWN,
                        {"element": self, "button_id": self.id},
                    )
                )
                return True

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.is_pressed:
                if self.howered:
                    pygame.event.post(
                        Event(
                            BUTTONUP,
                            {"element": self, "button_id": self.id},
                        )
                    )
                    return True
                self.is_pressed = False
                return True
        return False

    def draw(self, screen: Surface):
        if self.is_pressed and self.howered:
            self.background = self._active_bg
        elif self.howered:
            self.background = self._hover_bg
        else:
            self.background = self._normal_bg

        super().draw(screen)
