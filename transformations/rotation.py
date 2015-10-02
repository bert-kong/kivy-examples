__author__ = 'bckong'


from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.clock import Clock

import kivy.graphics.context_instructions as ctx
import kivy.graphics.vertex_instructions as vtx
import numpy as np
import os

width, height = Window.size
Window.clearcolor=(1, 1, 1, 1)


im_dir=os.path.join(os.path.dirname(os.path.dirname(__file__)),
                    "images")

class View(Widget):

    def __init__(self, **kw):
        super(View, self).__init__(**kw)

        self._angle=0
        self._sz=(100, 100)
        im=Image(source=os.path.join(im_dir, 'ninja_star.png'))

        with self.canvas:
            self._tr=ctx.Transform()
            self._rect=vtx.Rectangle(texture=im.texture,
                                     pos=(0, 0),
                                     size=self._sz)



    def update(self, dt):
        self._angle+=1
        x, y = self._sz

        # create a transform matrix(centered, angle)
        self._tr.identity()
        self._tr.translate(width/2, height/2, 0)
        self._tr.rotate(np.math.radians(self._angle),
                        0, 0, 1)
        self._tr.translate(-x/2, -y/2, 0)

        # debug
        if False:
            print self._tr.matrix



class UnitTest(App):

    def build(self):

        ui = View()
        Clock.schedule_interval(ui.update, 1./60.)

        return ui


if __name__=='__main__':

    UnitTest().run()