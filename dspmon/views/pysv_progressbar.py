__author__ = 'Bert Kong'
__version__ = '1.0.1'
__email__ = 'bert.x.kong@icloud.com'
__status__ = 'debug'

from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
import kivy.graphics.vertex_instructions as vtx
import kivy.graphics.context_instructions as ctx
from kivy.uix.widget import Widget
from kivy.clock import Clock
import os
import numpy as np


im_dir=r'C:\pydsp\monitor\res'
#im_dir=r'C:\Users\bckong\Pictures'
img_file_0=os.path.join(im_dir, 'devil-01.png')
img_file_1=os.path.join(im_dir, 'devil-02.png')


class ProgressBarAnimation(Widget):
    def __init__(self, **kw):
        super(ProgressBarAnimation, self).__init__(**kw)
        self._angle = 0
        self._radius = 10
        self._ratio = .5


        img = ( \
            Image(source=img_file_0),
            Image(source=img_file_1),
            )
        self._img = img

        size=self.image_size()

        # change the image center to origin (0, 0)
        devil = vtx.Rectangle(texture=img[0].texture,
                              size=size,
                              pos=(0, 0))

        self._devil = devil

        # ring radius

        # ring
        color = ctx.Color(0, 1, 1, 1., mode='rgba')
        x, y, r, _ = self.ring_pos_size()

        ring = vtx.Line(ellipse=(x, y, r, r, 0, 330), width=3)
        self._ring=ring

        # matrix
        self._rotation_tr = ctx.Transform()
        self._translate_tr = ctx.Transform()

        # -------------------------------------
        # graphics instructions
        # -------------------------------------

        # ring transformation
        self.canvas.add(ctx.PushMatrix())
        self.canvas.add(self._rotation_tr)
        self.canvas.add(color)
        self.canvas.add(ring)
        self.canvas.add(ctx.PopMatrix())

        # devil transformation
        #self.canvas.before.add(ctx.PushMatrix())
        #self.canvas.add(self._translate_tr)
        self.canvas.add(devil)
        #self.canvas.before.add(ctx.PopMatrix())


    def image_size(self):
        """
        widget size is used as base for size & position
        :return: (position, size)
        """

        w, h = self.size
        print "-------------> ", w, h
        w *=self._ratio
        h *=self._ratio
        print "-------------> ", w, h

        return (w, h)


    def ring_pos_size(self):
        """
        ring radius & position derived from the image size
        :return:
        """
        w, h=self.size
        w *=.7
        h *=.7
        x, y = -w/2, -h/2
        return (x, y, w, h)


    def update(self, dt):
        self._angle += 3

        if self._angle > 720:
            self._angle = 0

        if self._angle < 160:
            self._devil.texture = self._img[1].texture
        else:
            self._devil.texture = self._img[0].texture


        #------------------------------------
        #  rotation
        #------------------------------------
        x, y = self.pos
        w, h = self.size
        r_x = x + (w/2)
        r_y = y + (h/2)

        d_w, d_h = self._devil.size
        #print "size ", d_w, d_h
        #print "pos ", r_x, r_y
        x = (x + (w/2)) - (d_w/2)
        y = (y + (h/2)) - (d_h/2)

        self._devil.pos=(x, y)

        self._rotation_tr.identity()
        self._rotation_tr.translate(r_x, r_y, 0)
        self._rotation_tr.rotate(np.math.radians(self._angle), 0, 0, 1)


        #------------------------------------
        #  translate
        #------------------------------------
        #self._translate_tr.identity()
        #self._translate_tr.translate(100, 100, 0)

    def start(self, fr=1./60.):
        Clock.schedule_interval(self.update, fr)

    def stop(self):
        Clock.unschedule(self.update)


class View(BoxLayout):

    def __init__(self, **kw):
        super(View, self).__init__(**kw)

        self.orientation='vertical'
        #self.size_hint=(None, None)
        #self.size=(300, 300)
        devil=ProgressBarAnimation()

        label=Label(text="Start session, please wait")
        label.font_size=30
        label.size_hint=(1., 0.2)
        self.add_widget(label)
        self.add_widget(devil)

        devil.start()



class UnitTest(App):
    def build(self):
        view = View()



        return view


if __name__ == '__main__':
    UnitTest().run()
