from kivy.properties import DictProperty
from kivy.uix.screenmanager import ScreenManager
from importlib import import_module
from kivy.lang import Builder
from os.path import join, dirname, basename

from components.bar import win_md_bnb

Builder.load_file(join(dirname(__file__), basename(__file__).split(".")[0] + ".kv"))


class AppScreenManager(ScreenManager):
    """
    A custom ScreenManager that loads screens lazily.
    """
    screen_config = DictProperty(
        {
            "signup screen": {
                "presentation": ("features.signup.presentation", "SignupScreen")
            },
            "login screen": {
                "presentation": ("features.login.presentation", "LoginScreen")
            },
            "home screen": {
                "presentation": ("features.home.presentation", "HomeScreen")
            },
            "bookmark screen": {
                "presentation": ("features.bookmark.presentation", "BookmarkScreen")
            },
            "write screen": {
                "presentation": ("features.write.presentation", "WriteScreen")
            }
        }
    )

    def on_current(self, instance, value):
        """
        Loads a screen dynamically if it hasn't been loaded yet.
        """
        if value in ["menu screen", "login screen", "signup screen"] and win_md_bnb.bar:
            win_md_bnb.pop()
        if not self.has_screen(value):
            screen_data = self.screen_config[value]
            presentation_module_path, presentation_class_name = screen_data["presentation"]
            presentation_module = import_module(presentation_module_path)
            presentation_class = getattr(presentation_module, presentation_class_name)
            presentation = presentation_class()
            self.add_widget(presentation)
        supra = super().on_current(instance, value)
        if len(self.children) > 1:
            self.remove_widget(self.children[1])
        return supra

