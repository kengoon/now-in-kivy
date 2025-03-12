__all__ = ("Divider",)

from kivy.clock import Clock
from kivy.metrics import dp
from kivy.properties import ColorProperty, NumericProperty
from kivy.uix.boxlayout import BoxLayout

from kivy.lang import Builder
from os.path import join, dirname, basename

Builder.load_file(join(dirname(__file__), basename(__file__).split(".")[0] + ".kv"))


class Divider(BoxLayout):
    """
    A divider line.

    .. versionadded:: 2.0.0

    For more information, see in the
    :class:`~kivy.uix.boxlayout.BoxLayout` class documentation.
    """

    color = ColorProperty([.7, .7, .7, .5])
    """
    Divider color in (r, g, b, a) or string format.

    :attr:`color` is a :class:`~kivy.properties.ColorProperty`
    and defaults to `None`.
    """

    divider_width = NumericProperty(dp(1))
    """
    Divider width.

    :attr:`divider_width` is an :class:`~kivy.properties.NumericProperty`
    and defaults to `dp(1)`.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.on_orientation)

    def on_orientation(self, *args) -> None:
        """Fired when the values of :attr:`orientation` change."""

        if self.orientation == "vertical":
            self.size_hint_x = None
            self.width = self.divider_width
        elif self.orientation == "horizontal":
            self.size_hint_y = None
            self.height = self.divider_width
