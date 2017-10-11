__author__ = 'bckong'


from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.app import App
import os

__all__=( \
    'View',
    )

#im_dir=os.path.dirname(__file__)
#im_dir=os.path.join(im_dir, 'res')
im_dir=r'C:\pydsp\monitor\res'

class View(BoxLayout):

    def __init__(self, **kw):
        super(View, self).__init__(**kw)

        im_file=os.path.join(im_dir, 'mpeg_multiplexing_basic.png')
        im=Image(source=im_file)

        self.add_widget(im)




class UnitTest(App):

    def build(self):
        view=View()

        return view

if __name__=='__main__':
    UnitTest().run()



