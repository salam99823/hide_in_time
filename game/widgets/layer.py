from typing import List, Optional

from pygame import Rect

from game.types import ColorValue
from game.widgets import Align, Widget


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
