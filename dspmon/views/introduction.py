__author__ = 'bckong'


from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image

import kivy.graphics.context_instructions as ctx
import kivy.graphics.vertex_instructions as vtx

import view_properties as view_prop
import os

class Frame(object):

    def __init__(self, **kw):

        screen=kw.get('screen', None)
        r, g, b=kw.get('color', (1, 1, 1))

        color=ctx.Color(r, g, b)

        w, h=screen.size
        x, y=screen.pos
        x+=1; y+=1
        w-=2; h-=2

        rect=vtx.Line(rectangle=(x, y, w, h), width=.5)
        screen.canvas.add(color)
        screen.canvas.add(rect)
        self._rect=rect

        screen.bind(size=self.on_size_pos_change,
                    pos=self.on_size_pos_change)


    def on_size_pos_change(self, instance, value):
        w, h=instance.size
        x, y=instance.pos

        w-=2; h-=2; x+=1; y+=1

        self._rect.rectangle=(x, y, w, h)



im_dir=r'C:\pythonSV\broxton\vjt\display\sv\pydsp\monitor\res'

_images = ( \
     os.path.join(im_dir, 'bxt_display_datapath.png'),
)

class ScaledImage(Image):

    def __init__(self, **kw):
        super(ScaledImage, self).__init__(**kw)

        with self.canvas.before:
            ctx.PushMatrix()
            ctx.Scale(1.0, 1.0, 1.0)

        with self.canvas.after:
            ctx.PopMatrix()



class IntroPanel(Label):
    """
    BXT/BXT-P
    """

    def __init__(self, **kw):
        super(IntroPanel, self).__init__(**kw)

        text=kw.get('text', self.__doc__)
        self.text=text

        with self.canvas:
	    h, s, v = view_prop.table_color
            ctx.Color(h, s, v, mode='hsv')
            self._outline=vtx.Line(rectangle=self.rectangle(), width=1.0)

        self.bind(pos=self.on_pos_size_change,
                  size=self.on_pos_size_change)


    def on_pos_size_change(self, instance, value):
        self._outline.rectangle=self.rectangle()

    def rectangle(self):
        x, y=self.pos
        w, h=self.size

        w-=2; h-=2
        x+=1; y+=1

        return (x, y, w, h)



class Panel(BoxLayout):
    """
    Introduction main views:
        Image + Introduction

    """

    def __init__(self, **kw):
        super(Panel, self).__init__(**kw)
        self.orientation='vertical'
        self.padding=2
        self.spacing=2

        ratio=.2

        #-----------------------------------------
        #  Introduction/description
        #-----------------------------------------
        intro=IntroPanel()
        intro.size_hint=(1, ratio)
        intro.font_size=30
        self.add_widget(intro)
        self._intro=intro

        #-----------------------------------------
        #  Image
        #-----------------------------------------
        im=ScaledImage(source=_images[0])
        im.size_hint=(1., 1-ratio)
        self._im=im

        self.bind(size=self.on_pos_width_change,
                  pos=self.on_pos_width_change)
        self.add_widget(im)


    def on_pos_width_change(self, instance, value):
        win = self.get_parent_window()





class MyApp(App):
    def build(self):
        foo = Panel()

        return foo


if __name__ == '__main__':
    MyApp().run()
