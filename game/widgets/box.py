from enum import Enum
from typing import List

from pygame import Surface

from . import Widget, WidgetBuilder


class Direction(Enum):
    Horizontal = 0
    Vertical = 1


def HBox(*args, **kwargs) -> WidgetBuilder[Box]:
    return WidgetBuilder(Box, *args, direction=Direction.Horizontal, **kwargs)


def VBox(*args, **kwargs) -> WidgetBuilder[Box]:
    return WidgetBuilder(Box, *args, direction=Direction.Vertical, **kwargs)


class Box(Widget):
    childs: List[Widget]

    def __init__(
        self,
        childs: List[WidgetBuilder],
        direction: Direction = Direction.Horizontal,
        **kwargs,
    ) -> None:
        self.direction = direction
        super().__init__(**kwargs)
        self.childs = [child.build(self.padding) for child in childs]

    def realign(self):
        super().realign()
        match self.direction:
            case Direction.Horizontal:
                x = self.padding.x
                for child in self.childs:
                    deltax = child.margin.centerx - child.rect.centerx
                    deltay = child.margin.centery - child.rect.centery
                    deltax2 = child.margin.centerx - child.padding.centerx
                    deltay2 = child.margin.centery - child.padding.centery
                    child.margin.midleft = (
                        x,
                        self.padding.centery,
                    )
                    x += child.margin.width
                    child.rect.center = (
                        child.margin.centerx + deltax,
                        child.margin.centery + deltay,
                    )
                    child.padding.center = (
                        child.margin.centerx + deltax2,
                        child.margin.centery + deltay2,
                    )
            case Direction.Vertical:
                y = self.padding.y
                for child in self.childs:
                    deltax = child.margin.centerx - child.rect.centerx
                    deltay = child.margin.centery - child.rect.centery
                    deltax2 = child.margin.centerx - child.padding.centerx
                    deltay2 = child.margin.centery - child.padding.centery
                    child.margin.midtop = (self.padding.centerx, y)
                    y += child.margin.height
                    child.rect.center = (
                        child.margin.centerx + deltax,
                        child.margin.centery + deltay,
                    )
                    child.padding.center = (
                        child.margin.centerx + deltax2,
                        child.margin.centery + deltay2,
                    )
        for child in self.childs:
            child.realign()

    def focus(self, pos: tuple[int, int]):
        super().focus(pos)
        if self.focused:
            for child in self.childs:
                child.focus(pos)

    def draw(self, screen: Surface):
        super().draw(screen)
        for child in self.childs:
            child.draw(screen)
