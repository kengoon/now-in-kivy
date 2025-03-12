__all__ = ('OtpSheet',)

from kivy.animation import Animation
from kivy.clock import mainthread
from kivy.metrics import dp
from kivy.properties import VariableListProperty, NumericProperty, StringProperty, BooleanProperty
from kivy.clock import ClockEvent, Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from os.path import join, dirname, basename
from kivy.core.window import Window
from kivy.uix.modalview import ModalView

from components.behaviors import AdaptiveBehavior

Builder.load_file(join(dirname(__file__), basename(__file__).split(".")[0] + ".kv"))

clock: ClockEvent = None


class OtpSheet(BoxLayout, AdaptiveBehavior):
    __events__ = ("on_open", "on_dismiss", "on_submit_otp", "on_resend_otp")

    radius = VariableListProperty(["20dp", "20dp", 0, 0])
    timeout = NumericProperty(60)
    phone_number = StringProperty("08136346373")
    is_open = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        global clock
        self._countdown_callback = lambda _: setattr(self, "timeout", self.timeout - 1)
        clock = Clock.create_trigger(
            self._countdown_callback,
            timeout=1,
            interval=True
        )
        self.bind(timeout=lambda _, tmo: clock.cancel() if tmo == 0 else None)
        self.modalview = ModalView(
            background_color=(0, 0, 0, 0),
            background="",
            overlay_color=(0, 0, 0, .4),
            on_dismiss=lambda _: self.dismiss()
        )

    @mainthread
    def open(self):
        if self.is_open:
            return
        self.modalview.open()
        Window.add_widget(self)
        self._open()

    @mainthread
    def _open(self):
        anim = Animation(y=0, duration=.2)
        anim.bind(on_complete=lambda *_: clock())
        anim.start(self)
        self.is_open = True
        self.dispatch("on_open", self)

    @mainthread
    def dismiss(self):
        if not self.is_open:
            return
        anim = Animation(y=-self.height - dp(50), duration=.2)
        anim.bind(on_complete=self._dismiss)
        anim.start(self)
        self.is_open = False

    def _dismiss(self, *_):
        Window.remove_widget(self)
        self.modalview.dismiss()
        clock.cancel()

    def submit_otp(self):
        if self.ids.spinner.active:
            return
        self.ids.spinner.active = True
        otp = self.ids.otp.text
        self.dispatch("on_submit_otp", otp)

    def resend_otp(self):
        self.dispatch("on_resend_otp")
        self.timeout = self.property("timeout").defaultvalue
        clock()

    @mainthread
    def stop_spinner(self):
        self.ids.spinner.active = False

    def on_open(self, instance):
        ...

    def on_dismiss(self, instance):
        ...

    def on_submit_otp(self, otp):
        pass

    def on_resend_otp(self):
        pass

