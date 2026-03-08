from enum import Enum
from typing import Generic, Optional, Tuple, Type, TypeVar

from pygame import Rect, Surface, draw

from ..types import ColorValue


class Align(Enum):
    CENTER = 0
    TOP = 1
    BOTTOM = 2
    LEFT = 4
    RIGHT = 8
    TOPLEFT = TOP | LEFT
    BOTTOMLEFT = BOTTOM | LEFT
    TOPRIGHT = TOP | RIGHT
    BOTTOMRIGHT = BOTTOM | RIGHT


class Widget:
    """
    Base widget class
    """

    outer_rect: Rect
    parent: Rect
    maximize: Tuple[bool, bool]
    margin: Tuple[int, int, int, int] = (0, 0, 0, 0)
    padding: Tuple[int, int, int, int] = (0, 0, 0, 0)
    background: Optional[ColorValue]
    outline: Optional[tuple[ColorValue, int]]
    focused: bool = False

    def __init__(
        self,
        rect: Rect,
        parent: Rect,
        maximize: Tuple[bool, bool],
        margin: Tuple[int, int, int, int],
        padding: Tuple[int, int, int, int],
        background: Optional[ColorValue] = None,
        outline: Optional[tuple[ColorValue, int]] = None,
    ) -> None:
        self.parent = parent
        self.maximize = maximize
        if margin:
            self.margin = margin
        self.outer_rect = Rect(
            rect.x - self.margin[0],
            rect.y - self.margin[1],
            rect.width + self.margin[2],
            rect.height + self.margin[3],
        )
        if padding:
            self.padding = padding
        self.background = background
        self.outline = outline

    def get_rect(self) -> Rect:
        margin = self.margin
        return Rect(
            self.outer_rect.x + margin[0],
            self.outer_rect.y + margin[1],
            self.outer_rect.width - margin[2],
            self.outer_rect.height - margin[3],
        )

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
        self.outline = (color, width)

    def set_background(self, color: ColorValue):
        self.background = color

    def focus(self, pos: tuple[int, int]):
        """
        Sets widget focused if given point collides widget rect
        """
        self.focused = self.outer_rect.collidepoint(*pos)

    def draw(self, screen: Surface):
        "Draws widget and his childs on given surface"
        rect = self.get_rect()
        if self.background:
            draw.rect(screen, self.background, rect)
        draw.rect(screen, "Orange", self.outer_rect, 4)
        draw.rect(screen, "Pink", self.get_inner_rect(), 2)
        if self.outline:
            draw.rect(screen, self.outline[0], rect, self.outline[1])


WidgetType = TypeVar("WidgetType", bound=Widget)


def El(cls: Type[WidgetType], *args, **kwargs) -> WidgetBuilder[WidgetType]:
    return WidgetBuilder(cls, *args, **kwargs)


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
        outline: Optional[Tuple[ColorValue, int]] = None,
        **kwargs,
    ) -> None:
        super().__init__()
        self.widget_class = widget_class
        self.rect = rect
        self.maximize = maximize
        self.margin = margin
        self.padding = padding
        self.background = background
        self.outline = outline
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
            outline=self.outline,
            **self.kwargs,
        )
