from typing import List

from . import WidgetBuilder
from .box import Box


class LayerWidget(Box):
    pass


def Layer(childs: List[WidgetBuilder], *args, **kwargs) -> WidgetBuilder[LayerWidget]:
    return WidgetBuilder(LayerWidget, *args, childs=childs, **kwargs)
