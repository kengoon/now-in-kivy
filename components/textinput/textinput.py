__all__ = ('CustomTextInput',)

from kivy.lang import Builder
from os.path import join, dirname, basename
from kivy.properties import VariableListProperty, ColorProperty
from kivy.uix.textinput import TextInput

Builder.load_file(join(dirname(__file__), basename(__file__).split(".")[0] + ".kv"))


class CustomTextInput(TextInput):
    radius = VariableListProperty(0)
    bg_color = ColorProperty(None)
