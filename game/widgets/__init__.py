from enum import Enum
from typing import Any, Dict, Generic, List, Optional, Tuple, Type, TypeVar

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
    childs: List[Widget]
    align: Optional[Align] = None
    background: Optional[ColorValue]
    outline: Optional[tuple[ColorValue, int]]
    focused: bool = False

    def __init__(
        self,
        rect: Rect,
        parent: Rect,
        margin: Rect,
        padding: Rect,
        childs: List[Widget],
        align: Optional[Align],
        background: Optional[ColorValue] = None,
        outline: Optional[tuple[ColorValue, int]] = None,
    ) -> None:
        self.rect = rect
        self.parent = parent
        self.childs = childs
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

    def __setattr__(self, name: str, value: Any, /) -> None:
        super().__setattr__(name, value)
        if name == "align":
            self.realign()

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
        for child in self.childs:
            child.realign()

    def set_outline(self, color: ColorValue, width: int):
        self.outline = (color, width)

    def set_background(self, color: ColorValue):
        self.background = color

    def focus(self, pos: tuple[int, int]):
        """
        Sets widget focused if given point collides widget rect
        """
        self.focused = self.rect.collidepoint(*pos)
        if self.focused:
            for child in self.childs:
                child.focus(pos)

    def draw(self, screen: Surface):
        "Draws widget and his childs on given surface"
        if self.background:
            draw.rect(screen, self.background, self.rect)
        if self.outline:
            draw.rect(screen, self.outline[0], self.rect, self.outline[1])
        for child in self.childs:
            child.draw(screen)


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
    rect: Optional[Rect] = None
    margin: Optional[Rect] = None
    padding: Optional[Rect] = None
    childs: Optional[List[WidgetBuilder]] = None
    align: Optional[Align] = None
    background: Optional[ColorValue] = None
    outline: Optional[Tuple[ColorValue, int]] = None
    kwargs: Dict

    def __init__(
        self,
        widget_class: Type[WidgetType],
        rect: Optional[Rect] = None,
        margin: Optional[Rect] = None,
        padding: Optional[Rect] = None,
        childs: Optional[List[WidgetBuilder]] = None,
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
        self.childs = childs
        self.align = align
        self.background = background
        self.outline = outline
        self.kwargs = kwargs

    def build(self, parent: Rect):
        rect = self.rect if self.rect else parent
        margin = self.margin if self.margin else rect
        content_rect = self.padding if self.padding else rect
        childs = (
            [child.build(content_rect) for child in self.childs] if self.childs else []
        )
        return self.widget_class(
            rect=rect,
            parent=parent,
            margin=margin,
            padding=content_rect,
            childs=childs,
            align=self.align,
            background=self.background,
            outline=self.outline,
            **self.kwargs,
        )
