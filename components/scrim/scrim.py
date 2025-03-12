__all__ = ('DialogScrim',)

from kivy.properties import ColorProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.widget import Widget
from kivy.lang import Builder
from os.path import join, dirname, basename

Builder.load_file(join(dirname(__file__), basename(__file__).split(".")[0] + ".kv"))


class DialogScrim(ButtonBehavior, Widget):
    color = ColorProperty([0, 0, 0, 0.5])
