## Button Extra Behavior

The `ButtonExtraBehavior` [mixin](https://en.wikipedia.org/wiki/Mixin)
class adds the following features to the normal `Button` behavior:

#### Features

* **Long press:** An `on_long_press` event is emitted after a customizable
  `long_time`.

* **Right click:** An `on_right_click` event is emitted when pressing the
  mouse's right button.

* **Middle click:** An `on_middle_click` event is emitted when pressing the
  mouse's middle (scroll) button.

* **Double click:** An `on_double_click` event is emitted if a second click
  (tap) occurs inside a customizable `double_time`. This is disabled by
  default.
___

##### Usage

You can combine this class with a `Button` for a button that has everything,
or with the `ButtonBehavior` and other widgets, like an `Image` or even
Layouts, to provide alternative buttons that have Kivy button+extra behavior.

The `ButtonExtraBehavior` must be before `ButtonBehavior` or `Button` in a
[kivy mixin](https://kivy.org/doc/stable/api-kivy.uix.behaviors.html).

Because of the small delay that is added to the _single_ click when active
(equal to `double_time`), the "Double click" is disabled by default.

##### Attributes

* **long_time** - Minimum time that a click/press must be held, to be
  registered as a `long press`.  
  `long_time` is a `float` and defaults to 0.25.

* **double_time** - Maximum time for a second click/tap to be registered as
  `double click`.  
  `double_time` is a `float` and defaults to 0.2.

* **double_click_enabled** - Enables the double click detection. This
  introduces a delay to the `on_touch_down` emission in the case of a single
  click.  
  `double_click_enabled` is a `bool` and defaults to `False`.
___

##### Example

The following example adds the `ButtonExtraBehavior` to a `Button` and to an
`Image`. You can try the different clicking by looking at the top `Label`.

```python
from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from button_extra_behavior import ButtonExtraBehavior

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
        MyExtraImageButton:
            source: "data/logo/kivy-icon-256.png"
            double_click_enabled: True
            on_long_press: root.change_state(self, "Long press!")
            on_right_click: root.change_state(self, "Right click!")
            on_middle_click: root.change_state(self, "Middle click!")
            on_double_click: root.change_state(self, "Double click!")
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
```