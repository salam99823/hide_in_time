from typing import Tuple

from . import WidgetBuilder
from .box import Box


class LayerWidget(Box):
    pass


def Layer(
    childs: Tuple[WidgetBuilder, ...], *args, **kwargs
) -> WidgetBuilder[LayerWidget]:
    return WidgetBuilder(LayerWidget, *args, childs=childs, **kwargs)
