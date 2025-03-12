from kivy.core.window import Window as w
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import ListProperty, BooleanProperty, ColorProperty, StringProperty, VariableListProperty, \
    NumericProperty
from kivy.uix.behaviors import TouchRippleButtonBehavior, ButtonBehavior
from kivy.uix.relativelayout import RelativeLayout

from components.label import Badge, Icon, CustomLabel
from kivy.uix.boxlayout import BoxLayout
from os.path import join, dirname, basename

Builder.load_file(join(dirname(__file__), basename(__file__).split(".")[0] + ".kv"))

__all__ = ("NavigationBar", "NavigationItem", "base_bar", "win_md_bnb")


class NavigationItemLabel(CustomLabel):
    text_color_active = ColorProperty(None)
    text_color_normal = ColorProperty(None)


class NavigationItemIcon(Icon):
    icon_color_active = ColorProperty(None)
    icon_color_normal = ColorProperty(None)


class NavigationItem(ButtonBehavior, RelativeLayout):
    icon = StringProperty()
    icon_color_active = ColorProperty(None)
    icon_color_normal = ColorProperty(None)
    text = StringProperty()
    text_color_active = ColorProperty(None)
    text_color_normal = ColorProperty(None)
    use_text = BooleanProperty(True)
    use_badge = BooleanProperty(False)
    badge_text = StringProperty()
    ripple_effect = BooleanProperty(False)
    active = BooleanProperty(False)
    indicator_color = ColorProperty(None)
    indicator_transition = StringProperty("in_out_sine")
    indicator_duration = NumericProperty(0.1)
    _selected_region_width = NumericProperty(dp(0))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(lambda _: self.prepare_badge_and_text())

    def prepare_badge_and_text(self):
        icon = NavigationItemIcon(
            icon=self.icon,
            icon_color_normal=self.icon_color_normal,
            icon_color_active=self.icon_color_active
        )
        self.bind(
            icon=icon.setter("icon"),
            icon_color_normal=icon.setter("icon_color_normal"),
            icon_color_active=icon.setter("icon_color_active")
        )
        if self.use_badge:
            badge = Badge(text=self.badge_text)
            self.bind(
                badge_text=badge.setter("text"),
            )
            icon.add_widget(badge)
        self.add_widget(icon)
        if self.use_text:
            lbl = NavigationItemLabel(
                text=self.text,
                text_color_active=self.text_color_active,
                text_color_normal=self.text_color_normal
            )
            self.bind(
                text=lbl.setter("text"),
                text_color_normal=lbl.setter("text_color_normal"),
                text_color_active=lbl.setter("text_color_active"),
            )
            self.add_widget(lbl)

    def on_active(self, instance, value) -> None:
        """Fired when the values of :attr:`active` change."""

        def on_active(*args):
            Animation(
                _selected_region_width=dp(64) if value else 0,
                t=self.indicator_transition,
                d=self.indicator_duration,
            ).start(self)

        Clock.schedule_once(on_active)

    def on_release(self) -> None:
        """Fired when clicking on a panel item."""

        self.parent.set_active_item(self)

    def add_widget(self, widget, *args, **kwargs):
        if isinstance(widget, NavigationItemLabel):
            self.ids.label_container.add_widget(widget)
        elif isinstance(widget, NavigationItemIcon):
            self.ids.icon_container.add_widget(widget)
        else:
            return super().add_widget(widget)


class NavigationBar(BoxLayout):
    tabs = ListProperty()
    radius = VariableListProperty(0)
    use_text = BooleanProperty(True)
    indicator_color = ColorProperty(None)
    variant_icon = BooleanProperty(True)
    text_color_active = ColorProperty(None, allownone=True)
    text_color_normal = ColorProperty(None, allownone=True)
    icon_color_active = ColorProperty(None, allownone=True)
    icon_color_normal = ColorProperty(None, allownone=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(lambda _: self._add_tabs())

    def _add_tabs(self):
        for tab in self.tabs:
            btn = NavigationItem(
                text=tab["text"],
                badge_text=tab.get("badge_text", ""),
                use_badge=tab.get("use_badge", False),
                active=tab.get("active", False),
                indicator_color=self.indicator_color,
                on_release=tab.get("on_release", lambda _: None)
            )
            self._variant_assignment(btn, tab)
            if self.text_color_active:
                btn.text_color_active = self.text_color_active
            if self.text_color_normal:
                btn.text_color_normal = self.text_color_normal
            if self.icon_color_active:
                btn.icon_color_active = self.icon_color_active
            if self.icon_color_normal:
                btn.icon_color_normal = self.icon_color_normal
            btn.bind(on_release=self._switch_active)
            self.bind(
                text_color_normal=btn.setter("text_color_normal"),
                text_color_active=btn.setter("text_color_active"),
                icon_color_normal=btn.setter("icon_color_normal"),
                icon_color_active=btn.setter("icon_color_active")
            )
            self.add_widget(btn)

    def _switch_active(self, instance):
        for child, tab in zip(self.children[::-1], self.tabs):
            if child == instance:
                child.active = True
                child.icon = tab["icon"]
                continue
            child.active = False
            self._variant_assignment(child, tab)
        anim = Animation(y=dp(-5), d=.05) + Animation(y=0, d=.05)
        anim.start(instance)

    def _variant_assignment(self, btn, tab):
        if self.variant_icon and not btn.active:
            btn.icon = tab["icon_variant"]
        else:
            btn.icon = tab["icon"]

    def set_active_item(self, item: NavigationItem) -> None:
        """Sets the currently active element on the panel."""

        for widget in self.children:
            if item is widget:
                widget.active = True
            else:
                widget.active = False


class base_bar:
    bar = None
    state = "pop"
    bind_win_size_to_bar_pos = None
    _pop_listeners = []
    _push_listeners = []
    _push_height = 0
    _y = 0

    @classmethod
    def push(cls):
        cls.state = "push"
        for func in cls._push_listeners:
            func()

    @classmethod
    def pop(cls):
        cls.state = "pop"
        for func in cls._pop_listeners:
            func()

    @classmethod
    def remove_bnb(cls):
        cls.pop()
        w.remove_widget(cls.bar)
        cls.bar = None
        cls.bind_win_size_to_bnb_pos = None
        cls._pop_listeners.clear()
        cls._push_listeners.clear()

    @classmethod
    def _bind_win_size_width(cls):
        if cls.bar:
            w.bind(size=cls.bind_win_size_to_bar_pos)

    @classmethod
    def _unbind_win_size_width(cls):
        if cls.bar:
            w.unbind(size=cls.bind_win_size_to_bar_pos)

    @classmethod
    def register_listener(cls, **kwargs):
        if func := kwargs.get("pop"):
            cls._pop_listeners.append(func)
        if func := kwargs.get("push"):
            cls._push_listeners.append(func)


class win_md_bnb(base_bar):
    @classmethod
    def create_bnb(
            cls,
            bg_color=None,
            use_text=True,
            indicator_color=None,
            variant_icon=True,
            tabs=None,
            text_color_active=None,
            text_color_normal=None,
            icon_color_active=None,
            icon_color_normal=None,
            radius=0
    ):
        if cls.bar:
            return
        if tabs is None:
            tabs = []
        cls.bar = NavigationBar(
            tabs=tabs,
            variant_icon=variant_icon,
            indicator_color=indicator_color,
            use_text=use_text,
            text_color_active=text_color_active,
            text_color_normal=text_color_normal,
            icon_color_active=icon_color_active,
            icon_color_normal=icon_color_normal
        )
        if bg_color:
            cls.bar.bg_color = bg_color
        if radius is not None:
            cls.bar.radius = radius
        cls.bar.y = -cls.bar.height - dp(20)
        w.add_widget(cls.bar)

    @classmethod
    def push(cls):
        Animation(y=-0.5, d=.2).start(cls.bar)
        super().push()

    @classmethod
    def pop(cls):
        Animation(y=-cls.bar.height - dp(20), d=.2).start(cls.bar)
        super().pop()


if __name__ == "__main__":
    from kivy.app import App


    class TestApp(App):
        def on_start(self):
            win_md_bnb.create_bnb(
                tabs=[
                    {
                        "icon": "web",
                        "icon_variant": "web",
                        "text": "Discover",
                        "active": True,
                        "use_badge": True,
                        "badge_text": "900"
                    },
                    {
                        "icon": "fire-circle",
                        "icon_variant": "fire",
                        "text": "Memoir",
                    },
                    {
                        "icon": "dots-horizontal",
                        "icon_variant": "dots-horizontal",
                        "text": "More",
                    }
                ],
            )
            win_md_bnb.push()


    TestApp().run()
