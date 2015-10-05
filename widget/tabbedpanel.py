__author__ = 'leonardo'

from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.tabbedpanel import TabbedPanelItem
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.app import App
import os

import kivy_examples.transformations.sinewave as sinewave

im_dir=os.path.dirname(os.path.dirname(__file__))
print im_dir

im_file=os.path.join(im_dir, 'images/graphics_pipeline.png')

class MediaPanel(TabbedPanelItem):

    def __init__(self, **kwargs):
        super(MediaPanel, self).__init__(**kwargs)
        self.text='Media'

        layout=BoxLayout(orientation='vertical')
        #btn=Button(text="hello, world!")
        wave=sinewave.GeometryPad()
        wave.animate(True)

        layout.add_widget(wave)
        self.add_widget(layout)



class GraphicsPanel(TabbedPanelItem):

    def __init__(self, **kwargs):
        super(GraphicsPanel, self).__init__(**kwargs)
        self.text='Graphics'
        img=Image(source=im_file)
        self.add_widget(img)

class RootWidget(TabbedPanel):

    def __init__(self, **kw):
        super(RootWidget, self).__init__(**kw)
        self.do_default_tab=False
        tab_item_1=MediaPanel()
        tab_item_2=GraphicsPanel()

        self.add_widget(tab_item_1)
        self.add_widget(tab_item_2)




class UnitTest(App):

    def build(self):
        view=RootWidget()

        return view


if __name__=='__main__':
    UnitTest().run()