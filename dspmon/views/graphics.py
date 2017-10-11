__author__ = 'bckong'


from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.app import App
import os
import sys
sys.path.append(r'C:\Users\bckong\pyinst\dspmon')


import dspmon.views.sinewave as sinewave

im_dir=r'C:\PythonSv\broxton\vjt\display\sv\pydsp\monitor\res'
#im_dir=os.path.dirname(__file__)
#im_dir=os.path.join(im_dir, 'res')

class View(FloatLayout):

    def __init__(self, **kw):
        super(View, self).__init__(**kw)

        im_file=os.path.join(im_dir, 'graphics_pipeline.png')
        im=Image(source=im_file)

        wave=sinewave.GeometryPad()
        wave.size_hint=(.3, .3)
        wave.pos_hint={'top':1, 'right':1}
        wave.opacity=1
        wave.animate(True)
        #buttun=Button(text='Sine Wave')
        #buttun.size_hint=(.2, .2)
        #buttun.pos_hint={'top':1, 'right':1}

        self.add_widget(im)
        self.add_widget(wave)



class UnitTest(App):

    def build(self):
        view=View()

        return view

if __name__=='__main__':
    UnitTest().run()



