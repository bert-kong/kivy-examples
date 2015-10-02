__author__ = 'bckong'




from kivy.app import App
from kivy.properties import OptionProperty, NumericProperty, ListProperty, \
    BooleanProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from math import cos, sin
import kivy.graphics.context_instructions as ctx
import kivy.graphics.vertex_instructions as vtx
from kivy.core.window import Window
import numpy as np

w, h=Window.size


class GeometryPad(FloatLayout):

    _radius=NumericProperty(100)
    _points=ListProperty([0, 0, 0, 100])
    _points_sin=ListProperty([0, 0, w, h])
    _angle=NumericProperty(0)


    def __init__(self, **kwargs):
        super(GeometryPad, self).__init__(**kwargs)

        self._velocity=1
        self._time=0

        with self.canvas:

            ctx.PushMatrix()
            self._tr=ctx.Transform()
            ctx.Color(1.0, 0., 0, 1.0, mode='rgba')
            # center + radius
            vtx.Line(circle=(0, 0, self._radius), width=1)
            ctx.Color(1.0, 1., 1, 1.0, mode='rgba')
            self._line=vtx.Line(points=self._points, width=1)
            ctx.PopMatrix()

            # sin wave
            ctx.Color(0.0, 1., 0, 1.0, mode='rgba')
            ctx.PushMatrix()
            self._tr_sin=ctx.Transform()
            self._wave=vtx.Line(points=self._points_sin, width=1)
            ctx.PopMatrix()


    def update(self, delta):
        self._angle+=2 * 0.017
        self._time+=delta

        #----------------------------------------------
        self._tr.identity()
        self._tr.translate(150, 200, 0)
        self._tr.rotate(np.radians(self._angle), 0, 0, 1)
        self._tr.translate(0, 0, 0)

        points = []
        # radians

        np.set_printoptions(precision=2)
        X=np.arange(start=0, stop=self._angle, step=0.01)
        Y=np.sin(X)
        #print Y
        print "number of p ", len(X)
        for i in range(len(X)):
            points.append(X[i])
            points.append(Y[i] * 100)

        self._tr_sin.identity()
        self._tr_sin.translate(250, 200, 0)
        #self._points_sin=points
        self._wave.points=points

    def update_sin(self, dt):
        cy = self.height * 0.6
        cx = self.width * 0.1
        w = self.width * 0.8
        step = 20
        points = []
        self.dt += dt
        for i in range(int(w / step)):
            x = i * step
            points.append(cx + x)
            points.append(cy + sin(x / w * 8. + self.dt) * self.height * 0.2)

        self.points = points



    def animate(self, do_animation):
        if do_animation:
            Clock.schedule_interval(self.update, 1./60.)
        else:
            Clock.unschedule(self.update)


class UnitTest(App):

    def build(self):

        ui=GeometryPad()
        ui.animate(True)

        return ui

if __name__=='__main__':
    UnitTest().run()
