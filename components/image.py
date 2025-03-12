__all__ = ("CoverImage", )

from kivy.clock import Clock
from kivy.properties import StringProperty
from components.behaviors.stencil import StencilBehavior
from kivy.uix.image import AsyncImage


class CoverImage(AsyncImage, StencilBehavior):
    fit_mode = StringProperty("cover")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.clock = Clock.create_trigger(self.try_load_image, 1, True)

    def try_load_image(self, _):
        self.reload()
        self.clock.cancel()

    def on_load(self, *args):
        self.clock.cancel()

    def on_error(self, error):
        self.clock()
