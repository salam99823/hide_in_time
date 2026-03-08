from typing import Callable, Sequence, Tuple, Union

from pygame import Color

RGBAOutput = Tuple[int, int, int, int]
ColorValue = Union[Color, int, str, Tuple[int, int, int], RGBAOutput, Sequence[int]]
KeyCode = int
EventType = int
KeyEventType = int
KeyHandler = Union[Callable[[KeyEventType], None], None]
