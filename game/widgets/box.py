from enum import Enum
from typing import Tuple

from pygame import Surface

from . import Align, Widget, WidgetBuilder


class Direction(Enum):
    Horizontal = 0
    Vertical = 1


def HBox(*args, **kwargs) -> WidgetBuilder[Box]:
    return WidgetBuilder(Box, *args, direction=Direction.Horizontal, **kwargs)


def VBox(*args, **kwargs) -> WidgetBuilder[Box]:
    return WidgetBuilder(Box, *args, direction=Direction.Vertical, **kwargs)


class Box(Widget):
    childs: Tuple[Widget, ...]
    align_items: Align

    def __init__(
        self,
        childs: Tuple[WidgetBuilder, ...],
        direction: Direction = Direction.Vertical,
        align_items: Align = Align.CENTER,
        **kwargs,
    ) -> None:
        self.direction = direction
        self.align_items = align_items
        super().__init__(**kwargs)
        padding = self.get_inner_rect()
        self.childs = tuple(child.build(padding) for child in childs)
        self.resize_items()
        self.realign_items()

    def content_size(self) -> Tuple[int, int]:
        width = 0
        height = 0
        match self.direction:
            case Direction.Horizontal:
                for child in self.childs:
                    width += child.outer_rect.width
                    if child.outer_rect.height > height:
                        height = child.outer_rect.height
            case Direction.Vertical:
                for child in self.childs:
                    height += child.outer_rect.height
                    if child.outer_rect.width > width:
                        width = child.outer_rect.width
        return width, height

    def resize_items(self):
        if not self.childs:
            return
        padding = self.get_inner_rect()
        fixed_width = 0
        fixed_height = 0
        expand_width_count = 0
        expand_height_count = 0
        for child in self.childs:
            if child.outer_rect.width > padding.width:
                child.outer_rect.width = padding.width
            if child.outer_rect.height > padding.height:
                child.outer_rect.height = padding.height

            if child.maximize[0]:
                expand_width_count += 1
            else:
                fixed_width += child.outer_rect.width

            if child.maximize[1]:
                expand_height_count += 1
            else:
                fixed_height += child.outer_rect.height
        remaining_width = max(0, padding.width - fixed_width)
        remaining_height = max(0, padding.height - fixed_height)
        for child in self.childs:
            match self.direction:
                case Direction.Horizontal:
                    if child.maximize[0] and expand_width_count > 0:
                        child.outer_rect.width = remaining_width // expand_width_count
                    if child.maximize[1]:
                        child.outer_rect.height = padding.height
                case Direction.Vertical:
                    if child.maximize[0]:
                        child.outer_rect.width = padding.width
                    if child.maximize[1] and expand_height_count > 0:
                        child.outer_rect.height = (
                            remaining_height // expand_height_count
                        )
        for child in self.childs:
            if isinstance(child, Box):
                child.resize_items()

    def realign_items(self):
        if not self.childs:
            return
        padding = self.get_inner_rect()
        x = padding.left
        y = padding.top
        width, height = self.content_size()
        match self.direction:
            case Direction.Horizontal:
                match self.align_items:
                    case Align.TOP | Align.BOTTOM:
                        x = padding.centerx - width // 2
                        if self.align_items == Align.BOTTOM:
                            y = padding.bottom - height
                    case Align.LEFT | Align.RIGHT:
                        y = padding.centery - height // 2
                        if self.align_items == Align.RIGHT:
                            x = padding.right - width
                    case Align.TOPRIGHT:
                        x = padding.right - width
                    case Align.BOTTOMRIGHT:
                        y = padding.height - height
                        x = padding.right - width
                    case Align.BOTTOMLEFT:
                        y = padding.bottom - height
                    case Align.CENTER:
                        x = padding.centerx - width // 2
                        y = padding.centery - height // 2

                first = self.childs[0].outer_rect
                first.topleft = (x, y)
                midleft = first.midright
                for child in self.childs[1:]:
                    child.outer_rect.midleft = midleft
                    midleft = child.outer_rect.midright
            case Direction.Vertical:
                match self.align_items:
                    case Align.TOP | Align.BOTTOM:
                        x += (padding.right - width) // 2
                        if self.align_items == Align.BOTTOM:
                            y += padding.height - height
                    case Align.LEFT | Align.RIGHT:
                        y += (padding.height - height) // 2
                        if self.align_items == Align.RIGHT:
                            x += padding.width - width
                    case Align.TOPRIGHT:
                        x += padding.width - width
                    case Align.BOTTOMRIGHT:
                        y += padding.height - height
                        x += padding.width - width
                    case Align.BOTTOMLEFT:
                        y += padding.height - height
                    case Align.CENTER:
                        x += (padding.width - width) // 2
                        y += (padding.height - height) // 2

                first = self.childs[0].outer_rect
                first.topleft = (x, y)
                midtop = first.midbottom
                for child in self.childs[1:]:
                    child.outer_rect.midtop = midtop
                    midtop = child.outer_rect.midbottom
        for child in self.childs:
            if isinstance(child, Box):
                child.realign_items()

    def focus(self, pos: tuple[int, int]):
        super().focus(pos)
        if self.focused:
            for child in self.childs:
                child.focus(pos)

    def draw(self, screen: Surface):
        for child in self.childs:
            child.draw(screen)
