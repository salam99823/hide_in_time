from enum import Enum
from typing import Generic, Optional, Tuple, Type, TypeVar

import pygame
from pygame import Rect, Surface, draw
from pygame.event import Event

from ..types import ColorValue


class Widget:
    """
    Base widget class
    """

    outer_rect: Rect
    parent: Rect
    maximize: Tuple[bool, bool]
    margin: Tuple[int, int, int, int] = (0, 0, 0, 0)
    padding: Tuple[int, int, int, int] = (0, 0, 0, 0)
    border: Optional[tuple[ColorValue, int]]
    background: Optional[ColorValue]
    howered: bool = False

    def __init__(
        self,
        rect: Rect,
        parent: Rect,
        maximize: Tuple[bool, bool],
        margin: Tuple[int, int, int, int],
        padding: Tuple[int, int, int, int],
        border: Optional[tuple[ColorValue, int]] = None,
        background: Optional[ColorValue] = None,
    ) -> None:
        self.parent = parent
        self.maximize = maximize
        self.border = border
        self.background = background
        if margin:
            self.margin = margin
        self.outer_rect = Rect(
            rect.x - self.margin[0],
            rect.y - self.margin[1],
            rect.width + self.margin[2],
            rect.height + self.margin[3],
        )
        if border:
            border_width = border[1]
            self.outer_rect.x -= border_width
            self.outer_rect.y -= border_width
            self.outer_rect.width += border_width
            self.outer_rect.height += border_width
        if padding:
            self.padding = padding

    def get_rect(self) -> Rect:
        rect = self.outer_rect.move(self.margin[0], self.margin[1]).inflate(
            -self.margin[0] - self.margin[2], -self.margin[1] - self.margin[3]
        )
        if self.border:
            border_width = self.border[1]
            rect.x += border_width
            rect.y += border_width
            rect.width -= border_width
            rect.height -= border_width
        return rect

    def get_inner_rect(self) -> Rect:
        padding = self.padding
        rect = self.get_rect()
        return Rect(
            rect.x + padding[0],
            rect.y + padding[1],
            rect.width - padding[2],
            rect.height - padding[3],
        )

    def set_outline(self, color: ColorValue, width: int):
        self.border = (color, width)

    def set_background(self, color: ColorValue):
        self.background = color

    def handle_event(self, event: Event) -> bool:
        if event.type == pygame.MOUSEMOTION:
            self.howered = self.outer_rect.collidepoint(*event.pos)
            return self.howered
        return False

    def draw(self, screen: Surface):
        "Draws widget and his childs on given surface"
        rect = self.get_rect()
        if self.background:
            draw.rect(screen, self.background, rect)
        if self.border:
            draw.rect(screen, self.border[0], rect, self.border[1])


WidgetType = TypeVar("WidgetType", bound=Widget)


class WidgetBuilder(Generic[WidgetType]):
    """
    Generic widget builder

    ## Example

    ```python
    scenes = {
        GameState.MENU: Scene(
            (
                WidgetBuilder(
                    Layer,
                    childs=(
                        WidgetBuilder(
                            Widget,
                            Rect(0, 0, 300, 300),
                            childs=(
                                WidgetBuilder(
                                    Widget,
                                    Rect(0, 0, 100, 100),
                                    align=Align.RIGHT,
                                    outline=("Blue", 5),
                                )
                            ),
                            align=Align.CENTER,
                            outline=("Green", 5),
                        )
                    ),
                    outline=("Red", 5),
                )
            )
        )
    }
    ```
    """

    widget_class: Type[WidgetType]

    def __init__(
        self,
        widget_class: Type[WidgetType],
        rect: Optional[Rect] = None,
        maximize: Tuple[bool, bool] = (False, False),
        margin: Tuple[int, int, int, int] = (0, 0, 0, 0),
        padding: Tuple[int, int, int, int] = (0, 0, 0, 0),
        background: Optional[ColorValue] = None,
        border: Optional[Tuple[ColorValue, int]] = None,
        **kwargs,
    ) -> None:
        super().__init__()
        self.widget_class = widget_class
        self.rect = rect
        self.maximize = maximize
        self.margin = margin
        self.padding = padding
        self.background = background
        self.border = border
        self.kwargs = kwargs

    def build(self, parent: Rect):
        rect = self.rect if self.rect else parent
        if not self.rect:
            self.maximize = (True, True)
        return self.widget_class(
            rect=rect,
            parent=parent,
            maximize=self.maximize,
            margin=self.margin,
            padding=self.padding,
            background=self.background,
            border=self.border,
            **self.kwargs,
        )
