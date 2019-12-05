"""
Button Extra Behavior
=====================

The :class:`ButtonExtraBehavior` `mixin <https://en.wikipedia.org/wiki/Mixin>`_
class adds the following features to the :class:`~kivy.uix.button.Button`
behavior:

Features
========

* **Long press:** An `on_long_press` event is emitted after a customizable
  `long_time`.

* **Right click:** An `on_right_click` event is emitted when pressing the
  mouse's right button.

* **Middle click:** An `on_middle_click` event is emitted when pressing the
  mouse's middle (scroll) button.

* **Double click:** An `on_double_click` event is emitted if a second click
  (tap) occurs inside a customizable `double_time`. This is disabled by
  default.

* **Scroll Up:** An `on_scroll_up` event is emitted when the mouse wheel
  scrolls up.

* **Scroll Down:** An `on_scroll_up` event is emitted when the mouse wheel
  scrolls down.

You can combine this class with a :class:`~kivy.uix.button.Button`
for a button that has everything, or with
:class:`~kivy.uix.behaviors.button.ButtonBehavior` and other widgets, like an
:class:`~kivy.uix.image.Image` or even Layouts, to provide alternative buttons
that have Kivy button+extra behavior.

The :class:`ButtonExtraBehavior` must be _before_
:class:`~kivy.uix.button.Button` or
:class:`~kivy.uix.behaviors.button.ButtonBehavior` in a
`kivy mixin <https://kivy.org/doc/stable/api-kivy.uix.behaviors.html>`_

Because of the small delay that is added to the *single* click when active (equal
to `double_time`), the "Double click" is disabled by default.


Example
_______

You can try the different clicks if you run this module directly.

"""
from kivy.properties import BooleanProperty, NumericProperty
from kivy.clock import Clock


__author__ = "noEmbryo"
__version__ = "0.6.0.0"

__all__ = ("ButtonExtraBehavior",)


# noinspection PyAttributeOutsideInit,PyUnresolvedReferences
class ButtonExtraBehavior(object):
    """ This `mixin <https://en.wikipedia.org/wiki/Mixin>`_ class adds
    right/middle/double/long click/press/scroll events to any widget.

    :Events:
        `on_long_press`
            Fired after the button is held for more than a customizable
            `long_time`.
        `on_right_click`
            Fired when the right button of a mouse is pressed.
        `on_middle_click`
            Fired when the middle (scroll) button of a mouse is pressed
        `on_double_click`
            Fired if a second click (tap) occurs inside a customizable
            `double_time`. This is disabled by default.
        `on_scroll_up`
            Fired when the mouse wheel scrolls up.
        `on_scroll_down`
            Fired when the mouse wheel scrolls down.
    """

    long_time = NumericProperty(.25)
    """ Minimum time that a click/press must be held, to be registered
    as a `long press`.

    :attr:`long_time` is a float and defaults to 0.25.
    """

    double_time = NumericProperty(.2)
    """ Maximum time for a second click/tap to be registered as `double click`.

    :attr:`double_time` is a float and defaults to 0.2.
    """

    double_click_enabled = BooleanProperty(False)
    """ Enables the double click detection. This introduces a delay to the
    `on_touch_down` emission in the case of a single click.
    
    :attr:`double_click_enabled` is a :class:`~kivy.properties.BooleanProperty`
    and defaults to `False`.
    """

    def __init__(self, **kwargs):
        super(ButtonExtraBehavior, self).__init__(**kwargs)
        self.register_event_type("on_double_click")
        self.register_event_type("on_middle_click")
        self.register_event_type("on_right_click")
        self.register_event_type("on_long_press")
        self.register_event_type("on_scroll_up")
        self.register_event_type("on_scroll_down")

        self.after_long_press = False
        self.long_clock = Clock.schedule_once(self.long_pressed,
                                              self.long_time)
        self.long_clock.cancel()

        self.second_click = False
        self.double_clock = Clock.schedule_once(self.send_press,
                                                self.double_time)
        self.double_clock.cancel()

    def on_touch_down(self, touch):
        for child in self.children[:]:
            if child.dispatch("on_touch_down", touch):
                return True
        if self.collide_point(*touch.pos):
            self.after_long_press = False
            self.second_click = False
            if "button" in touch.profile:
                if touch.button == "right":
                    self.dispatch("on_right_click")
                    self.state = "down"
                    return True  # block release if right click is emitted
                elif touch.button == "middle":
                    self.state = "down"
                    self.dispatch("on_middle_click")
                    return True  # block release if middle click is emitted
                elif touch.button == "scrollup":
                    self.dispatch("on_scroll_up")
                    return True  # block release if scroll up is emitted
                elif touch.button == "scrolldown":
                    self.dispatch("on_scroll_down")
                    return True  # block release if scroll down is emitted

            if self.double_clock.is_triggered:  # if double click
                self.second_click = True
                self.state = "down"
                self.double_clock.cancel()
                self.dispatch("on_double_click")
                return True  # block release if double click is emitted
            elif self.double_click_enabled:  # don't check for double click
                self.double_clock()
            else:
                super(ButtonExtraBehavior, self).on_touch_down(touch)
            self.long_clock()
            return True

    def on_touch_up(self, touch, *__):
        for child in self.children[:]:
            if child.dispatch("on_touch_up", touch):
                return True
        if self.collide_point(*touch.pos):
            self.state = "normal"
            if "button" in touch.profile and touch.button in ["scrollup", "scrolldown"]:
                return True  # just block scroll release
            if self.long_clock.is_triggered:
                self.long_clock.cancel()
                if self.double_click_enabled:
                    return True  # block release while waiting for double click
            else:
                if self.second_click:
                    return True  # block release if double click is emitted
                if self.after_long_press:
                    return True  # block release if long press is emitted
            super(ButtonExtraBehavior, self).on_touch_up(touch)
            return True

    def send_press(self, *__):
        """ Propagates the `touch_down` event
        """
        try:
            if not self.long_clock.is_triggered:
                super(ButtonExtraBehavior, self).trigger_action()
            else:
                self.state = "down"
        except AttributeError:  # no ButtonBehavior in MixIn
            pass

    def long_pressed(self, *__):
        """ Sends the "on_long_press" event
        """
        self.after_long_press = True
        self.dispatch("on_long_press")

    def on_long_press(self):
        """ Needed for the "on_long_press" event """

    def on_right_click(self):
        """ Needed for the "on_right_click" event """

    def on_middle_click(self):
        """ Needed for the "on_middle_click" event """

    def on_double_click(self):
        """ Needed for the "on_double_click" event """

    def on_scroll_up(self):
        """ Needed for the "on_scroll_up" event """

    def on_scroll_down(self):
        """ Needed for the "on_scroll_down" event """


if __name__ == "__main__":

    from kivy.app import App
    from kivy.uix.image import Image
    from kivy.uix.popup import Popup
    from kivy.uix.button import Button
    from kivy.uix.boxlayout import BoxLayout
    from kivy.lang import Builder

    Builder.load_string("""
<Base>
    orientation: "vertical"
    Label:
        id: label
        size_hint_y: 3
        text: "Try the different type of clicks on the Button and the Image"
    BoxLayout:
        size_hint_y: 7
        MyExtraButton:
            text: "Button"
            double_click_enabled: True
            on_press: root.change_state(self, "Button press")
            on_release: root.change_state(self, "Button release")
            on_long_press: root.change_state(self, "Long press!")
            on_right_click: root.change_state(self, "Right click!")
            on_middle_click: root.change_state(self, "Middle click!")
            on_double_click: root.change_state(self, "Double click!")
            on_scroll_up: root.change_state(self, "Scroll up!")
            on_scroll_down: root.change_state(self, "Scroll down!")
        MyExtraImageButton:
            source: "data/logo/kivy-icon-256.png"
            double_click_enabled: True
            on_long_press: root.change_state(self, "Long press!")
            on_right_click: root.change_state(self, "Right click!")
            on_middle_click: root.change_state(self, "Middle click!")
            on_double_click: root.change_state(self, "Double click!")
            on_scroll_up: root.change_state(self, "Scroll up!")
            on_scroll_down: root.change_state(self, "Scroll down!")
""")


    class Base(BoxLayout):
        def __init__(self, **kwargs):
            super(Base, self).__init__(**kwargs)
            self.popup = Popup()

        def change_state(self, widget, text):
            kind = "Button" if isinstance(widget, Button) else "Kivy Image"
            self.ids.label.text = ("Last click was on the {} and it was a {}"
                                   .format(kind, text))


    class MyExtraButton(ButtonExtraBehavior, Button):
        pass


    class MyExtraImageButton(ButtonExtraBehavior, Image):
        pass


    class SampleApp(App):

        def build(self):
            return Base()


    SampleApp().run()
