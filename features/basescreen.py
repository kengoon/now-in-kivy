from kivy.clock import mainthread
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen

from libs.singleton import screen_extras


class BaseScreen(Screen):
    data_source = ObjectProperty(None)

    @mainthread
    def toast(self, text, length_long=True):
        from kvdroid.tools import toast
        toast(text, length_long)

    @staticmethod
    def put_extra(key, value):
        screen_extras[key] = value

    @staticmethod
    def get_extra(key, default=None):
        return screen_extras.get(key, default)

    @staticmethod
    def remove_extra(key):
        del screen_extras[key]
