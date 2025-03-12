from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty, NumericProperty, ColorProperty, BooleanProperty
from kivy.lang import Builder
from ui.theme import Theme
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.lang import Builder
from os.path import join, dirname, basename

Builder.load_file(join(dirname(__file__), basename(__file__).split(".")[0] + ".kv"))


class Card(Theme, BoxLayout):
    bg_color = ColorProperty()
    radius = ListProperty([0, 0, 0, 0])
    shadow_radius = ListProperty([0, 0, 0, 0])
    elevation = NumericProperty(0.16)
    shadow_distance_x = NumericProperty(- dp(5))
    shadow_distance_y = NumericProperty(- dp(5))
    shadow_blur = NumericProperty(dp(10))
    shadow_x = NumericProperty(0)
    shadow_y = NumericProperty(- dp(2))
    outline = BooleanProperty(False)
    outline_width = NumericProperty(0.6)

