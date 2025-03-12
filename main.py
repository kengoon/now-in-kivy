from kivy import platform
from kivy.app import App
from kivy.core.window import Window
from kivy.loader import Loader
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import FadeTransition

from components.bar import win_md_bnb
from ui.theme import ThemeManager
from components.factory_register import register_factory
from features.screenmanager import AppScreenManager
from kivy.lang import Builder

Loader.error_image = "assets/images/transparent.png"
Loader.loading_image = "assets/images/transparent.png"
# Window.softinput_mode = "below_target"
Builder.load_file("imports.kv")
register_factory()


class ChollofApp(App):
    theme_cls = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sm = None
        self.theme_cls = ThemeManager()
        # self.theme_cls.theme_style = "Dark"
        if platform == "android":
            from kvdroid.tools import change_statusbar_color, navbar_color
            change_statusbar_color(
                self.theme_cls.bg_color[:3],
                "black" if self.theme_cls.theme_style == "Light" else "white"
            )
            navbar_color(
                self.theme_cls.bg_color
            )
            self.theme_cls.bind(
                theme_style=lambda _, value: (
                    change_statusbar_color(
                        self.theme_cls.bg_color,
                        "black" if value == "Light" else "white"
                    ),
                    navbar_color(
                        self.theme_cls.bg_color
                    )
                )
            )

    def build(self):
        transition = FadeTransition(clearcolor=self.theme_cls.bg_color, duration=.1)
        self.theme_cls.bind(
            bg_color=transition.setter("clearcolor")
        )
        self.sm = sm = AppScreenManager(transition=transition)
        # if platform == "android":
        #     from sjfirebase.tools.mixin import UserMixin
        #     if user := UserMixin().get_current_user():
        #         user.reload()
        sm.current = "home screen"
        return sm

    def on_start(self):
        win_md_bnb.create_bnb(
            tabs=[
                {
                    "icon": "inbox",
                    "icon_variant": "inbox-outline",
                    "text": "For you",
                    "active": True,
                    "on_release": lambda _: setattr(self.sm, "current", "home screen")
                },
                {
                    "icon": "bookmark-multiple",
                    "icon_variant": "bookmark-multiple-outline",
                    "text": "Saved",
                    "active": False,
                    "on_release": lambda _: setattr(self.sm, "current", "bookmark screen")
                },
                {
                    "icon": "square-edit-outline",
                    "icon_variant": "square-edit-outline",
                    "text": "Write",
                    "on_release": lambda _: setattr(self.sm, "current", "write screen")
                }
            ],
        )
        win_md_bnb.push()


if __name__ == '__main__':
    ChollofApp().run()
