from dataclasses import dataclass
from enum import Enum
from typing import Generic, List, Optional, Tuple, Type, TypeVar

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
    rect: Rect
    parent: Rect
    childs: List[Widget]
    margin: int
    padding: int
    align: Optional[Align] = None
    background: Optional[ColorValue]
    outline: Optional[tuple[ColorValue, int]]
    focused: bool = False

    def __init__(
        self,
        rect: Rect,
        parent: Rect,
        childs: List[Widget],
        align: Optional[Align],
        margin: int = 1,
        padding: int = 0,
        background: Optional[ColorValue] = None,
        outline: Optional[tuple[ColorValue, int]] = None,
    ) -> None:
        self.rect = rect
        self.parent = parent
        self.childs = childs
        if align:
            self.set_align(align)
        self.margin = margin
        self.padding = padding
        self.background = background
        self.outline = outline

    def set_align(self, align: Align):
        self.align = align
        match self.align:
            case Align.CENTER:
                self.rect.center = self.parent.center
            case Align.TOP:
                self.rect.top = self.parent.top
                self.rect.centerx = self.parent.centerx
            case Align.BOTTOM:
                self.rect.bottom = self.parent.bottom
                self.rect.centerx = self.parent.centerx
            case Align.LEFT:
                self.rect.left = self.parent.left
                self.rect.centery = self.parent.centery
            case Align.RIGHT:
                self.rect.right = self.parent.right
                self.rect.centery = self.parent.centery
            case Align.TOPLEFT:
                self.rect.topleft = self.parent.topleft
            case Align.BOTTOMLEFT:
                self.rect.bottomleft = self.parent.bottomleft
            case Align.TOPRIGHT:
                self.rect.topright = self.parent.topright
            case Align.BOTTOMRIGHT:
                self.rect.bottomright = self.parent.bottomright

    def set_outline(self, color: ColorValue, width: int):
        self.outline = (color, width)

    def set_background(self, color: ColorValue):
        self.background = color

    def focus(self, pos: Optional[tuple[int, int]] = None):
        if pos and self.rect:
            self.focused = self.rect.collidepoint(*pos)
            if self.focused:
                for child in self.childs:
                    child.focus(pos)

    def draw(self, screen: Surface):
        if self.background:
            draw.rect(screen, self.background, self.rect)
        if self.outline:
            draw.rect(screen, self.outline[0], self.rect, self.outline[1])
        for child in self.childs:
            child.draw(screen)


WidgetType = TypeVar("WidgetType", bound=Widget)


@dataclass
class WidgetBuilder(Generic[WidgetType]):
    widget_class: Type[WidgetType]
    rect: Optional[Rect] = None
    childs: Optional[List[WidgetBuilder]] = None
    align: Optional[Align] = None
    background: Optional[ColorValue] = None
    outline: Optional[Tuple[ColorValue, int]] = None

    def with_rect(self, rect):
        self.rect = rect

    def with_childs(self, childs):
        self.childs = childs

    def with_align(self, align):
        self.align = align

    def with_background(self, background):
        self.background = background

    def with_outline(self, outline):
        self.outline = outline

    def build(self, parent: Rect):
        rect = self.rect if self.rect else parent
        childs = [child.build(rect) for child in self.childs] if self.childs else []
        return self.widget_class(
            rect=rect,
            parent=parent,
            childs=childs,
            align=self.align,
            background=self.background,
            outline=self.outline,
        )
