__author__ = 'bxkong'




import numpy as np
from kivy.app import App
from kivy.properties import NumericProperty, ListProperty
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.clock import Clock
import kivy.graphics.context_instructions as ctx
import kivy.graphics.vertex_instructions as vtx
from kivy.core.window import Window

w, h=Window.size


class GeometryPad(Widget):

    _radius=NumericProperty(100)
    _points=ListProperty([0, 0, 100, 0])
    _points_sin=ListProperty([0, 0, w, h])
    _angle=NumericProperty(0)


    def __init__(self, **kwargs):
        super(GeometryPad, self).__init__(**kwargs)
        self._velocity=1
        self._x_axis=(0, 0, w, 0)
        self._y_axis=(0, 0, 0, h)

        self._coord_height=400

        with self.canvas:
            #-------------------------------------
            # X-Y Coordinate
            #-------------------------------------
            ctx.PushMatrix()
            self._tr_coord=ctx.Translate(150, self._coord_height, 0)
            self._label=Label(text="182 degree")
            ctx.Color(0.0, 0., 1, 1.0, mode='rgba')
            vtx.Line(points=self._x_axis, width=1)
            vtx.Line(points=self._y_axis, width=1)
            ctx.PopMatrix()

            ctx.PushMatrix()
            self._tr=ctx.Transform()

            #  circle + radius
            ctx.Color(1.0, 0., 0, 1.0, mode='rgba')
            vtx.Line(circle=(0, 0, self._radius), width=2)

            ctx.Color(0.0, 0.0, 0.0, 1.0, mode='rgba')
            self._line=vtx.Line(points=self._points, width=2)
            ctx.PopMatrix()

            #-------------------------------------
            #  sin wave
            #-------------------------------------
            ctx.Color(0.0, 1., 0, 1.0, mode='rgba')
            ctx.PushMatrix()
            self._tr_sin=ctx.Transform()
            self._wave=vtx.Line(points=self._points_sin, width=2)
            ctx.PopMatrix()


    def update(self, delta):
        # in degree
        self._angle=(self._angle+self._velocity)%540

        self._label.text="%d degree" % (self._angle, )
        #----------------------------------------------
        self._tr.identity()
        self._tr.translate(150, self._coord_height, 0)
        self._tr.rotate(np.radians(self._angle), 0, 0, 1)

        points = []
        # radians

        np.set_printoptions(precision=2)
        X=np.arange(start=0, stop=self._angle, step=1)
        Y=np.sin(np.radians(X))

        #print Y
        for i in range(len(X)):
            points.append(X[i])
            points.append(Y[i] * 100)

        self._tr_sin.identity()
        self._tr_sin.translate(250, self._coord_height, 0)
        #self._points_sin=points
        self._wave.points=points



    def animate(self, do_animation):
        if do_animation:
            Clock.schedule_interval(self.update, 1./30.)
        else:
            Clock.unschedule(self.update)


class UnitTest(App):

    def build(self):

        ui=GeometryPad()
        ui.animate(True)

        return ui

if __name__=='__main__':
    UnitTest().run()
