from typing import Optional, Tuple

import pygame
from pygame import Rect, Surface
from pygame.font import Font

from game.types import ColorValue

from . import Widget, WidgetBuilder


def Label(text: str, *args, **kwargs) -> WidgetBuilder[LabelWidget]:
    return WidgetBuilder(LabelWidget, *args, text=text, **kwargs)


class LabelWidget(Widget):
    _text: str
    _font: Font
    _color: ColorValue
    text_surface: Surface

    def __init__(
        self,
        rect: Rect,
        text: str,
        parent: Rect,
        maximize: Tuple[bool, bool],
        margin: Tuple[int, int, int, int],
        padding: Tuple[int, int, int, int],
        color: ColorValue = "Black",
        font_famiy: Optional[str] = None,
        font_size: int = 48,
        border: Optional[tuple[ColorValue, int]] = None,
        background: Optional[ColorValue] = None,
    ) -> None:
        super().__init__(rect, parent, maximize, margin, padding, border, background)

        self._text = text
        self._font = pygame.font.SysFont(font_famiy, font_size)
        self._color = color
        self.redraw_surface()

    def redraw_surface(self):
        self.text_surface = self.font.render(self._text, True, self._color)

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, text: str):
        self._text = text
        self.redraw_surface()

    @property
    def font(self) -> Font:
        return self._font

    @font.setter
    def font(self, font: Font):
        self._font = font
        self.redraw_surface()

    @property
    def color(self) -> ColorValue:
        return self._color

    @color.setter
    def color(self, color: ColorValue):
        self._color = color
        self.redraw_surface()

    def draw(self, screen: Surface):
        super().draw(screen)
        inner_rect = self.get_inner_rect()
        text_rect = self.text_surface.get_rect(center=inner_rect.center)
        screen.blit(self.text_surface, text_rect)
