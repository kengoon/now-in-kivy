__all__ = ("CustomLabel", "Icon", "Badge")

from kivy.core.clipboard import Clipboard
from kivy.properties import BooleanProperty, StringProperty, VariableListProperty, \
    ColorProperty
from kivy.uix.label import Label
from components.behaviors import AdaptiveBehavior
from kivy.lang import Builder
from os.path import join, dirname, basename

Builder.load_file(join(dirname(__file__), basename(__file__).split(".")[0] + ".kv"))


class CustomLabel(AdaptiveBehavior, Label):
    __events__ = ("on_copy",)
    allow_copy = BooleanProperty(False)
    bg_color = ColorProperty("#00000000")
    radius = VariableListProperty(0)

    def on_long_touch(self, touch, *args) -> None:
        if self.allow_copy and self.collide_point(*touch.pos):
            Clipboard.copy(self.text)
            self.dispatch("on_copy")

    def on_copy(self) -> None:
        pass


class Icon(CustomLabel):
    icon = StringProperty()
    font_name = StringProperty("assets/fonts/materialdesignicons-webfont.ttf")


class Badge(CustomLabel):
    pass
