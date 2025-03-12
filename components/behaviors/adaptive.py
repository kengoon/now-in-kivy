__all__ = ("AdaptiveBehavior",)

from kivy.properties import BooleanProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen


class AdaptiveBehavior:
    adaptive_height = BooleanProperty(False)
    """
    If `True`, the following properties will be applied to the widget:

    .. code-block:: kv

        size_hint_y: None
        height: self.minimum_height

    :attr:`adaptive_height` is an :class:`~kivy.properties.BooleanProperty`
    and defaults to `False`.
    """

    adaptive_width = BooleanProperty(False)
    """
    If `True`, the following properties will be applied to the widget:

    .. code-block:: kv

        size_hint_x: None
        width: self.minimum_width

    :attr:`adaptive_width` is an :class:`~kivy.properties.BooleanProperty`
    and defaults to `False`.
    """

    adaptive_size = BooleanProperty(False)
    """
    If `True`, the following properties will be applied to the widget:

    .. code-block:: kv

        size_hint: None, None
        size: self.minimum_size

    :attr:`adaptive_size` is an :class:`~kivy.properties.BooleanProperty`
    and defaults to `False`.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setter_widget_size = None
        self.setter_widget_height = None
        self.setter_label_height = None
        self.setter_widget_width = None
        self.setter_label_width = None

    def on_adaptive_height(self, _, value: bool) -> None:
        self.size_hint_y = None if value else 1
        if not (self.setter_label_height and self.setter_widget_height):
            self.setter_label_height = lambda *x: self.setter("height")(
                self, self.texture_size[1]
            )
            self.setter_widget_height = self.setter("height")
        if isinstance(self, Label):
            if value:
                self.bind(texture_size=self.setter_label_height)
            else:
                self.unbind(texture_size=self.setter_label_height)
        else:
            if not isinstance(self, (FloatLayout, Screen)):
                if value:
                    self.bind(minimum_height=self.setter_widget_height)
                    if not self.children:
                        self.height = 0
                else:
                    self.bind(minimum_height=self.setter_widget_height)

    def on_adaptive_width(self, _, value: bool) -> None:
        self.size_hint_x = None if value else 1
        if not (self.setter_label_width and self.setter_widget_width):
            self.setter_label_width = lambda *x: self.setter("width")(
                self, self.texture_size[0]
            )
            self.setter_widget_width = self.setter("width")

        if isinstance(self, Label):
            if value:
                self.bind(texture_size=self.setter_label_width)
            else:
                self.unbind(texture_size=self.setter_label_width)
        else:
            if not isinstance(self, (FloatLayout, Screen)):
                if value:
                    self.bind(minimum_width=self.setter_widget_width)
                    if not self.children:
                        self.width = 0
                else:
                    self.unbind(minimum_width=self.setter_widget_width)

    def on_adaptive_size(self, _, value: bool) -> None:
        self.size_hint = (None, None) if value else (1, 1)
        self.setter_widget_size = self.setter("size")

        if value:
            if isinstance(self, Label):
                self.text_size = (None, None)
                self.bind(texture_size=self.setter_widget_size)
            else:
                if not isinstance(self, (FloatLayout, Screen)):
                    self.bind(minimum_size=self.setter("size"))
                    if not self.children:
                        self.size = (0, 0)
        else:
            self.unbind(minimum_size=self.setter_widget_size)