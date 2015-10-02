__author__ = 'bckong'

import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.clock import Clock

im_dir=r"C:\Users\bckong\Pictures"

im_file=os.path.join(im_dir, 'bxtp.png')

class MyButton(Button):

    def __init__(self, **kw):
        super(MyButton, self).__init__(**kw)

        im=Image(source=im_file)
        self._im=im

        self.bind(pos=self.on_pos_change)
        self.bind(size=self.on_pos_change)

    def on_pos_change(self, instance, value):
        print "pos, center ", self.pos, self.center
        self._im.center=self.center

    def on_touch_down(self, touch):
        print "ID ===> ", id(touch)

        self.add_widget(self._im)


    def on_touch_move(self, touch):
        pass

    def on_touch_up(self, touch):
        print "ID ===> ", id(touch)

        self.remove_widget(self._im)



class View(BoxLayout):

    def __init__(self, **kw):
        super(View, self).__init__(**kw)
        self.orientation='vertical'

        btn=MyButton()
        self.add_widget(btn)


class UnitTest(App):

    def build(self):

        view=View()
        return view




if __name__=='__main__':
    UnitTest().run()