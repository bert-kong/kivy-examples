__author__ = 'Bertrand Kong'
__copyrights__ = 'Intel Corp. 2014, BXT Project'
__version__ = '1.0.1'
__email__ = 'bertrand.c.kong@intel.com'
__status__ = 'debug'



from kivy.app import App
from kivy.uix.image import Image
import kivy.graphics.vertex_instructions as vtx
import kivy.graphics.context_instructions as ctx
from kivy.uix.widget import Widget
from kivy.clock import Clock
import numpy as np

img_file_0=r'C:\Users\bckong\Pictures\devil-01.png'
img_file_1=r'C:\Users\bckong\Pictures\devil-03.png'

class MyProgressBar(Widget):

    def __init__(self, **kw):
        super(MyProgressBar, self).__init__(**kw)
        self._angle=0

        img = ( \
            Image(source=img_file_0),
            Image(source=img_file_1),
            )

        self._img=img

        # widget size
        w, h = self.size

        # image size
        im_w, _=img[0].size

        # change the image center to origin (0, 0)
        im_x = -im_w/2.
        devil=vtx.Rectangle(texture=img[0].texture,
                            size=(im_w, im_w),
                            pos=(im_x, im_x))

        self._devil=devil

        # ring radius
        radius=im_w + 20
        print "radius --> ", radius
        self._radius=radius

        # ring
        color=ctx.Color(0, 1, 1, 1., mode='rgba')
        r_x, r_y = (-radius/2, -radius/2)
        ring=vtx.Line(ellipse=(r_x, r_y, radius, radius, 0, 330), width=3)

        # matrix
        self._rotation_tr=ctx.Transform()
        self._translate_tr=ctx.Transform()


        #-------------------------------------
        # graphics instructions
        #-------------------------------------

        # ring transformation
        self.canvas.add(ctx.PushMatrix())
        self.canvas.add(self._rotation_tr)
        self.canvas.add(color)
        self.canvas.add(ring)
        self.canvas.add(ctx.PopMatrix())

        # devil transformation
        self.canvas.before.add(ctx.PushMatrix())
        self.canvas.add(self._translate_tr)
        self.canvas.add(devil)
        self.canvas.before.add(ctx.PopMatrix())



    def update(self, dt):
        self._angle+=1


        if self._angle>720:
            self._angle=0

        if self._angle<80:
            self._devil.texture=self._img[1].texture
        else:
            self._devil.texture=self._img[0].texture



        #self._ring_tr.translate(395+(self._radius/2), 300+(self._radius/2), 0)
        self._rotation_tr.identity()
        self._rotation_tr.translate(100, 100, 0)
        self._rotation_tr.rotate(np.math.radians(self._angle), 0, 0, 1)

        self._translate_tr.identity()
        self._translate_tr.translate(100, 100, 0)





class UnitTest(App):

    def build(self):

        view=MyProgressBar()

        Clock.schedule_interval(view.update, 1/60.)
        return view


if __name__=='__main__':
    UnitTest().run()



