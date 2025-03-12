__all__ = ("CustomCheckbox",)

from kivy.properties import StringProperty, AliasProperty
from kivy.uix.behaviors import TouchRippleBehavior, ToggleButtonBehavior
from components.label import Icon
from kivy.lang import Builder
from os.path import join, dirname, basename

Builder.load_file(join(dirname(__file__), basename(__file__).split(".")[0] + ".kv"))


class CustomCheckbox(ToggleButtonBehavior, TouchRippleBehavior, Icon):
    checkbox_icon_normal = StringProperty("checkbox-blank-outline")
    checkbox_icon_down = StringProperty("checkbox-marked")

    def _get_active(self):
        return self.state == 'down'

    def _set_active(self, value):
        self.state = 'down' if value else 'normal'

    active = AliasProperty(
        _get_active, _set_active, bind=('state', ), cache=True)

    def __init__(self, **kwargs):
        self.fbind('state', self._on_state)
        super().__init__(**kwargs)

    def _on_state(self, instance, value):
        if self.group and self.state == 'down':
            self._release_group(self)

    def on_group(self, *args):
        super().on_group(*args)
        if self.active:
            self._release_group(self)
