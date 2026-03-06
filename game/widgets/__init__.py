from enum import Enum
from typing import Dict, Generic, Optional, Tuple, Type, TypeVar

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

    ## Example

    ```python
    class Layer(Widget):
        def __init__(
            self,
            parent: Rect,
            childs: List[Widget],
            align: Optional[Align] = None,
            outline: Optional[tuple[ColorValue, int]] = None,
            **_,
        ) -> None:
            super().__init__(parent, parent, childs=childs, align=align, outline=outline)
    ```
    """

    rect: Rect
    parent: Rect
    margin: Rect
    padding: Rect
    align: Align = Align.CENTER
    background: Optional[ColorValue]
    outline: Optional[tuple[ColorValue, int]]
    focused: bool = False

    def __init__(
        self,
        rect: Rect,
        parent: Rect,
        margin: Rect,
        padding: Rect,
        align: Optional[Align] = None,
        background: Optional[ColorValue] = None,
        outline: Optional[tuple[ColorValue, int]] = None,
    ) -> None:
        self.rect = rect
        self.parent = parent
        if margin:
            self.margin = margin
        else:
            self.margin = rect
        if padding:
            self.padding = padding
        else:
            self.padding = rect
        if align:
            self.align = align
        self.background = background
        self.outline = outline

    def realign(self):
        deltax = self.margin.centerx - self.rect.centerx
        deltay = self.margin.centery - self.rect.centery
        deltax2 = self.margin.centerx - self.padding.centerx
        deltay2 = self.margin.centery - self.padding.centery
        match self.align:
            case Align.CENTER:
                self.margin.center = self.parent.center
            case Align.TOP:
                self.margin.midtop = self.parent.midtop
            case Align.BOTTOM:
                self.margin.midbottom = self.parent.midbottom
            case Align.LEFT:
                self.margin.midleft = self.parent.midleft
            case Align.RIGHT:
                self.margin.midright = self.parent.midright
            case Align.TOPLEFT:
                self.margin.topleft = self.parent.topleft
            case Align.BOTTOMLEFT:
                self.margin.bottomleft = self.parent.bottomleft
            case Align.TOPRIGHT:
                self.margin.topright = self.parent.topright
            case Align.BOTTOMRIGHT:
                self.margin.bottomright = self.parent.bottomright
        self.rect.center = (
            self.margin.centerx + deltax,
            self.margin.centery + deltay,
        )
        self.padding.center = (
            self.margin.centerx + deltax2,
            self.margin.centery + deltay2,
        )

    def set_outline(self, color: ColorValue, width: int):
        self.outline = (color, width)

    def set_background(self, color: ColorValue):
        self.background = color

    def focus(self, pos: tuple[int, int]):
        """
        Sets widget focused if given point collides widget rect
        """
        self.focused = self.rect.collidepoint(*pos)

    def draw(self, screen: Surface):
        "Draws widget and his childs on given surface"
        if self.background:
            draw.rect(screen, self.background, self.rect)
        draw.rect(screen, "Orange", self.margin, 4)
        draw.rect(screen, "Pink", self.padding, 4)
        if self.outline:
            draw.rect(screen, self.outline[0], self.rect, self.outline[1])


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
            [
                WidgetBuilder(
                    Layer,
                    childs=[
                        WidgetBuilder(
                            Widget,
                            Rect(0, 0, 300, 300),
                            childs=[
                                WidgetBuilder(
                                    Widget,
                                    Rect(0, 0, 100, 100),
                                    align=Align.RIGHT,
                                    outline=("Blue", 5),
                                )
                            ],
                            align=Align.CENTER,
                            outline=("Green", 5),
                        )
                    ],
                    outline=("Red", 5),
                )
            ]
        )
    }
    ```
    """

    widget_class: Type[WidgetType]
    args: Tuple
    kwargs: Dict

    def __init__(
        self,
        widget_class: Type[WidgetType],
        rect: Optional[Rect] = None,
        margin: Optional[Rect] = None,
        padding: Optional[Rect] = None,
        align: Optional[Align] = None,
        background: Optional[ColorValue] = None,
        outline: Optional[Tuple[ColorValue, int]] = None,
        **kwargs,
    ) -> None:
        super().__init__()
        self.widget_class = widget_class
        self.rect = rect
        self.margin = margin
        self.padding = padding
        self.align = align
        self.background = background
        self.outline = outline
        self.kwargs = kwargs

    def build(self, parent: Rect):
        rect = self.rect if self.rect else parent
        margin = self.margin if self.margin else rect
        padding = self.padding if self.padding else rect
        widget = self.widget_class(
            rect=rect,
            parent=parent,
            margin=margin,
            padding=padding,
            background=self.background,
            outline=self.outline,
            **self.kwargs,
        )
        widget.realign()
        return widget
