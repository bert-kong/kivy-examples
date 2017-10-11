__author__ = 'bckong'

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
import kivy.graphics.vertex_instructions as vtx
import kivy.graphics.context_instructions as ctx


about_text="""
Real-Time Display Monitoring Tool 1.0.3
usage :
        - SVN update C:/PythonSv/broxton/vjt/display
        - click the dspmon icon to launch the app from
          display directory

contact : bertrand.c.kong@intel.com
"""


class View(BoxLayout):
    left=ObjectProperty()
    right=ObjectProperty()

    def __init__(self, **kw):
        super(View, self).__init__(**kw)

        self.orientation='horizontal'

        self.left=BoxLayout(orientaion='vertical')
        self.left.padding=2
        self.right=BoxLayout(orientaion='vertical')
        self.add_widget(self.left)
        self.add_widget(self.right)


        label=Label(text=about_text)
        self.label=label

        label.pos_hint={'top':1, }
        label.size_hint=(1., .3)
        #label.bind(size=self.on_size_change)
        label.bind(size=self.on_pos_size_change)
        label.bind(pos=self.on_pos_size_change)


        self.rectangle=vtx.Line(rectangle=self.rectangle_geometry())

        label.canvas.add(ctx.Color(0, 1, 1, 1))
        label.canvas.add(self.rectangle)

        #label.size_hint=(.5, .5)
        #label.pos_hint={'center_x':.4}
        self.left.add_widget(label)

    def on_size_change(self, instance, value):
        instance.text_size=instance.size

    def on_pos_size_change(self, instance, value):
        self.rectangle.rectangle=self.rectangle_geometry()

    def rectangle_geometry(self):
        x, y=self.label.pos
        w, h=self.label.size

        return (x, y, w, h)

class UnitTest(App):
    def build(self):
        view = View()

        return view


if __name__ == '__main__':
    UnitTest().run()
