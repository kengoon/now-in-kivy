__all__ = ("BlogList", "pre_compute_data")

from kivy.metrics import sp, dp
from kivy.properties import StringProperty, ListProperty
from kivy.uix.behaviors import TouchRippleButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from os.path import join, dirname, basename

from libs import compute_text_size

Builder.load_file(join(dirname(__file__), basename(__file__).split(".")[0] + ".kv"))


def pre_compute_data(widget, data):
    for value in data:
        summary_height = compute_text_size(
            text=value["summary"],
            font_size=sp(16),
            padding=[0, 0, 0, 0],
            widget_width=widget.width - dp(60),
            line_height=1.24
        )[1]
        title_height = compute_text_size(
            text=value["title"],
            font_size=sp(24),
            padding=[0, 0, 0, 0],
            widget_width=widget.width - dp(130),
            line_height=1.32
        )[1]
        value["_size"] = [0, dp(170) + summary_height + title_height + dp(80) + sp(11)]
    return data


class BlogList(TouchRippleButtonBehavior, BoxLayout):
    _size = ListProperty([0, 0])
    image = StringProperty("")
    title = StringProperty("")
    date = StringProperty("")
    post_type = StringProperty("")
    summary = StringProperty("")