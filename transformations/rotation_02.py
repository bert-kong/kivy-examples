__author__ = 'bckong'

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.properties import NumericProperty
from kivy.graphics.instructions import Callback

import kivy.graphics.context_instructions as ctx
import kivy.graphics.vertex_instructions as vtx
import numpy as np
import os

width, height = Window.size
Window.clearcolor=(1, 1, 1, 1)


im_dir=os.path.join(os.path.dirname(os.path.dirname(__file__)),
                    "images")

class View(Widget):

    angle=NumericProperty(0)

    def __init__(self, **kw):
        super(View, self).__init__(**kw)

        self._angle=0
        self._sz=(100, 100)
        im=Image(source=os.path.join(im_dir, 'ninja_star.png'))

        with self.canvas:
            #ctx.PushMatrix()


            self._rt=ctx.Rotate()
            self._rt.angle=0
            self._rt.origin=(width/2, height/2)

            rect=vtx.Rectangle(texture=im.texture,
                               pos=(0, 0),
                               size=self._sz)

        #with self.canvas.after:
        #    ctx.PopMatrix()

    def mycallback(self, instr):
        print "callback", self._angle
        self._rt.angle=self._angle

    def update(self, dt):
        self._angle+=1
        self._rt.angle=self._angle
        print self._rt.origin
        self.canvas.ask_update()



class UnitTest(App):

    def build(self):

        ui = View()
        Clock.schedule_interval(ui.update, 1./60.)

        return ui


if __name__=='__main__':
    UnitTest().run()

