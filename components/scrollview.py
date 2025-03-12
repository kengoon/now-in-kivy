from kivy.graphics import Color, PushMatrix, Scale, PopMatrix
from kivy.uix.recycleview import RecycleView
from kivy.clock import Clock
from kivy.properties import OptionProperty, BooleanProperty, ObjectProperty, NumericProperty, ListProperty
from kivy.animation import Animation
from components.behaviors import StencilBehavior

from components.effects import LowerScrollEffect, LowerDampedScrollEffect

__all__ = ("LEFT", "RIGHT", "DOWN", "UP", "NULL", "RealRecycleView")

LEFT = 1  # finger and content moves right (scroll bar moves left) to see the far left of the entire content
RIGHT = 2  # finger and content moves left (scroll bar moves right) to see the far right of the entire content
DOWN = 3  # finger and content moves up (scroll bar moves down) to see the very bottom of the entire content
UP = 4  # finger and content moves down (scroll bar moves up) to see the very top of the entire content
NULL = 0  # finger or scroll bar or content is not moving


class RealRecycleView(RecycleView):
    do_swipe = BooleanProperty(False)
    swipe_direction = OptionProperty("horizontal", options=["horizontal", "vertical"], allownone=False)
    effect_cls = ObjectProperty(LowerDampedScrollEffect, allownone=True)
    scroll_distance_traveled = ListProperty([0, 0])  # read only
    scroll_direction = NumericProperty(NULL)  # read only
    track_scroll_movement = BooleanProperty(False)

    _swipe_right_listeners = []
    _swipe_left_listeners = []
    _swipe_down_listeners = []
    _swipe_up_listeners = []
    _internal_scale = None

    def __init__(self, **kwargs):
        self.register_event_type('on_real_scroll_stop')  # type: ignore
        self.register_event_type("on_real_scroll_start")
        self.register_event_type("on_swipe_up")
        self.register_event_type("on_swipe_down")
        self.register_event_type("on_swipe_left")
        self.register_event_type("on_swipe_right")
        self.register_event_type("on_overscroll")
        self.register_event_type("on_overscroll_down")
        self.register_event_type("on_overscroll_up")
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(rgba=[0, 0, 0, 1])
            PushMatrix()
            self._internal_scale = Scale()
        with self.canvas.after:
            PopMatrix()
        self.effect_y.scale_axis = "y"
        self.effect_x.scale_axis = "x"

        self.scroll_index = 0
        self._scrolling = False
        self._clock = Clock.create_trigger(self.check_scrolling, 1, True)
        self._start_touch = None
        self._is_touch_move = False
        self.__scroll_y = self.scroll_y
        self.__scroll_x = self.scroll_x
        Clock.schedule_once(self.on_data)

    def on_scroll_move(self, touch):
        if supra := super().on_scroll_move(touch):
            self._is_touch_move = True
            if self.track_scroll_movement:
                self._clock()
        return supra

    def on_scroll_start(self, touch, check_children=True):
        if supra := super().on_scroll_start(touch, check_children):
            self.dispatch("on_real_scroll_start")
            self._start_touch = touch.pos
        return supra

    def on_scroll_stop(self, touch, check_children=True):
        if supra := super().on_scroll_stop(touch, check_children):
            self.get_swipe_direction(touch)
        return supra

    def get_swipe_direction(self, touch):
        checks = all([self.do_swipe, self._start_touch, self._is_touch_move])
        if checks:
            if self.swipe_direction == "horizontal":
                if self._start_touch[0] < touch.pos[0]:
                    self.swipe_right()
                    self.dispatch("on_swipe_right")
                else:
                    self.swipe_left()
                    self.dispatch("on_swipe_left")
            elif self._start_touch[1] < touch.pos[1]:
                self.swipe_up()
                self.dispatch("on_swipe_up")
            else:
                self.swipe_down()
                self.dispatch("on_swipe_down")

        self._start_touch = None
        self._is_touch_move = False

    def on_data(self, *_):
        if self.swipe_direction == "vertical":
            self.scroll_index = len(self.data) - 1

    def swipe_up(self):
        if not self.children:
            return
        if self.scroll_index > 0 < len(self.data) - 1:
            self.scroll_index -= 1
            child_height = self.children[0].default_height
            scroll = self.convert_distance_to_scroll(0, child_height * self.scroll_index)[1]
            anim = Animation(scroll_y=max(scroll, 0.0), t='out_quad', d=.3)
            anim.bind(on_complete=lambda *_: self.dispatch_listeners(direction="up"))
            anim.start(self)

    def swipe_down(self):
        if not self.children:
            return
        if self.scroll_index < len(self.data) - 1:
            self.scroll_index += 1
            child_height = self.children[0].default_height
            scroll = self.convert_distance_to_scroll(0, child_height * self.scroll_index)[1]
            anim = Animation(scroll_y=min(scroll, 1.0), t='out_quad', d=.3)
            anim.bind(on_complete=lambda *_: self.dispatch_listeners(direction="down"))
            anim.start(self)

    def swipe_left(self):
        if not self.children:
            return
        if self.scroll_index < len(self.data) - 1:
            self.scroll_index += 1
            child_width = self.children[0].default_width
            scroll = self.convert_distance_to_scroll(child_width * self.scroll_index, 0)[0]
            anim = Animation(scroll_x=min(scroll, 1.0), t='out_quad', d=.3)
            anim.bind(on_complete=lambda *_: self.dispatch_listeners(direction="left"))
            anim.start(self)

    def swipe_right(self):
        if not self.children:
            return
        if self.scroll_index > 0 < len(self.data):
            self.scroll_index -= 1
            child_width = self.children[0].default_width
            scroll = self.convert_distance_to_scroll(child_width * self.scroll_index, 0)[0]
            anim = Animation(scroll_x=max(scroll, 0.0), t='out_quad', d=.3)
            anim.bind(on_complete=lambda *_: self.dispatch_listeners(direction="right"))
            anim.start(self)

    def on_scroll_y(self, *_):
        if self.__scroll_y > self.scroll_y:
            self.scroll_direction = DOWN
        else:
            self.scroll_direction = UP
        self.__scroll_y = self.scroll_y
        self._scrolling = True
        viewport = self.get_viewport()
        viewport_scroll_height = self.viewport_size[1] - viewport[-1]
        self.scroll_distance_traveled = viewport[0], viewport_scroll_height - viewport[1]

    def on_scroll_x(self, *_):
        if self.__scroll_x < self.scroll_x:
            self.scroll_direction = RIGHT
        else:
            self.scroll_direction = LEFT
        self.__scroll_x = self.scroll_x
        self._scrolling = True
        viewport = self.get_viewport()
        self.scroll_distance_traveled = viewport[0], viewport[1]

    def check_scrolling(self, *_):
        if not self._scrolling:
            self._clock.cancel()
            self.dispatch("on_real_scroll_stop")
            self.scroll_direction = NULL
        self._scrolling = False

    @classmethod
    def register_swipe_listener(cls, **kwargs):
        if func := kwargs.get("up"):
            cls._swipe_up_listeners.append(func)
        if func := kwargs.get("down"):
            cls._swipe_down_listeners.append(func)
        if func := kwargs.get("left"):
            cls._swipe_left_listeners.append(func)
        if func := kwargs.get("right"):
            cls._swipe_right_listeners.append(func)
        else:
            raise AttributeError(f"Unknown argument. Argument must be any or both of [up, down, right, left]")

    @classmethod
    def unregister_swipe_listener(cls, **kwargs):
        if func := kwargs.get("up"):
            cls._swipe_up_listeners.remove(func)
        if func := kwargs.get("down"):
            cls._swipe_down_listeners.remove(func)
        if func := kwargs.get("left"):
            cls._swipe_left_listeners.remove(func)
        if func := kwargs.get("right"):
            cls._swipe_right_listeners.remove(func)
        else:
            raise AttributeError(f"Unknown argument. Argument must be any or both of [up, down, right, left]")

    def dispatch_listeners(self, direction):
        if direction == "up":
            for func in self._swipe_up_listeners:
                func()
        elif direction == "down":
            for func in self._swipe_down_listeners:
                func()
        elif direction == "left":
            for func in self._swipe_left_listeners:
                func()
        else:
            for func in self._swipe_right_listeners:
                func()

    def on_touch_down(self, touch):
        self.effect_x.last_touch_pos = touch.pos
        self.effect_y.last_touch_pos = touch.pos
        super().on_touch_down(touch)

    def on_touch_move(self, touch):
        self.effect_x.convert_overscroll(touch)
        self.effect_y.convert_overscroll(touch)
        super().on_touch_move(touch)

    def on_touch_up(self, touch):
        self.effect_x.reset_scale()
        self.effect_y.reset_scale()
        super().on_touch_up(touch)

    def on_real_scroll_stop(self):
        pass

    def on_real_scroll_start(self):
        pass

    def on_swipe_up(self):
        pass

    def on_swipe_down(self):
        pass

    def on_swipe_left(self):
        pass

    def on_swipe_right(self):
        pass

    def on_overscroll(self, *args):
        pass

    def on_overscroll_down(self):
        pass

    def on_overscroll_up(self):
        pass
