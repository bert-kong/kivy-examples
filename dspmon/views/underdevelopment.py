__author__ = 'bxkong'

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.app import App

import os

im_dir = r'C:\pydsp\monitor\res'
im_file = os.path.join(im_dir, 'underdevelopment_2.png')


# im_dir=r'C:\Users\bckong\Pictures'
# im_file=os.path.join(im_dir, 'office-dog.gif')

class Panel(BoxLayout):
    def __init__(self, **kw):
        super(Panel, self).__init__(**kw)
        self.orientation = 'vertical'

        label = Label(text="Under Development")
        label.size_hint=(1., .2)
        label.font_size = 30
        self.add_widget(label)

        im = Image(source=im_file)
        self.add_widget(im)


# -----------------------------------
#  Unit Test
# -----------------------------------
class UnitTest(App):
    def build(self):
        view = Panel()

        return view


if __name__ == '__main__':
    UnitTest().run()
