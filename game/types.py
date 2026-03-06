from typing import Callable, Sequence, Tuple, Union

from pygame import KEYDOWN, KEYUP, Color

RGBAOutput = Tuple[int, int, int, int]
ColorValue = Union[Color, int, str, Tuple[int, int, int], RGBAOutput, Sequence[int]]
KeyCode = int
EventType = int
KeyEventType = KEYDOWN | KEYUP
KeyHandler = Union[Callable[[KeyEventType], None], None]
