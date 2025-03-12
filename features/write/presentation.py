from os.path import join, dirname, basename
from kivy.app import App
from kivy.clock import triggered, mainthread
from kivy.lang import Builder
from kivy.metrics import dp

from features.basescreen import BaseScreen
from libs.decorator import android_only

Builder.load_file(join(dirname(__file__), basename(__file__).split(".")[0] + ".kv"))


class WriteScreen(BaseScreen):
    @android_only
    @triggered(.2)
    def push_up_textinput(self, focus):
        from kvdroid.tools import check_keyboad_visibility_and_get_height

        if focus:
            self.ids.divider.color = App.get_running_app().theme_cls.primary_color
        else:
            self.ids.divider.color = self.ids.divider.property("color").defaultvalue
        visible, height = check_keyboad_visibility_and_get_height()
        self.children[0].padding = [0, 0, 0, height or dp(80)]
