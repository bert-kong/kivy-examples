__author__ = 'Bertrand Kong'
__copyrights__ = 'Intel Corp. 2014, BXT Project'
__version__ = '1.0.1'
__email__ = 'bertrand.c.kong@intel.com'
__status__ = 'debug'


import os
from kivy.core.image import Image
from kivy.core.window import Window
from kivy.uix.widget import Widget
import kivy.vector as vt
import kivy.graphics.vertex_instructions as vtx
from kivy.app import App

gWidth, gHeight = Window.size

class Sprite(object):

    def __init__(self, img_src, width, height):

        self.texture = Image(img_src).texture
        self._width = width
        self._height = height

    def get_region(self, x, y):
        return self.texture.get_region(x, y, self._width, self._height)


#------------------------------------------
#
#------------------------------------------
img_path = r'C:\images\game'
class Boy(object):

    def __init__(self, canvas):

        # image file
        img_src = os.path.join(img_path, 'boys.png')
        print "image file ---> ", img_src
        self._sprite = Sprite(img_src, 64, 64)

        #-------------------------------
        # start position
        #-------------------------------
        self._pos = vt.Vector(gWidth/2, 10)
        self._vel = vt.Vector(4, 0)

        #-------------------------------
        # left region
        #-------------------------------
        self._texer_region_pos = vt.Vector(0, 64)
        self._texer_off = 64

        #-------------------------------
        # rectangle instance with boy texture
        #-------------------------------
        texture = self._sprite.get_region(0, 64)
        body = vtx.Rectangle(texture=texture, pos=self._pos)
        self._body = body

        # add draw command to canvas
        self._canvas = canvas.add(body)

    #----------------------------
    #  position
    #----------------------------
    @property
    def position(self):
        return self._pos

    #----------------------------
    #  velocity
    #----------------------------
    @property
    def velocity(self):
        return self._vel

    @velocity.setter
    def velocity(self, vel):
        """

        :param vel: (x, y
        :return:
        """
        self._vel = vt.Vector(vel)


    def move_to(self, direction):
        """

        :param direction: left or right
        :return:
        """

        #------------------------------
        if direction=='left':
            self._vel.x = self._vel.x if self._vel.x<0 else -1 * self._vel.x
            self._texer_region_pos.y=64

        #------------------------------
        elif direction=='right':
            self._vel.x = self._vel.x if self._vel.x>0 else -1 * self._vel.x
            self._texer_region_pos.y=0


        #------------------------------
        # update position
        #------------------------------
        self._pos += self._vel

        #------------------------------
        # texture region
        #------------------------------
        self._texer_region_pos.x += self._texer_off

        # reset region
        if self._texer_region_pos.x<0:
            self._texer_region_pos.x = 64
        elif self._texer_region_pos.x>512:
            self._texer_region_pos.x = 64

        # get the region in the texture
        texture = self._sprite.get_region(self._texer_region_pos.x,
                                          self._texer_region_pos.y)

        # update boy state for canvas
        self._body.pos = self._pos
        self._body.texture = texture

    def remove_canvas(self):
        self._canvas.remove(self._body)
        self._canvas = None


class TestGui(App):

    def build(self):
        gui = Widget()

        self._boy = Boy(gui.canvas)
        self._boy.velocity = (6, 0)
        keyboard = Window.request_keyboard(None, self)
        keyboard.bind(on_key_down=self.on_keydown)

        return gui

    def on_keydown(self, keyboard, keycode, text, modifies):

        if keycode[1]=='left':
            self._boy.move_to('left')
        elif keycode[1]=='right':
            self._boy.move_to('right')

if __name__=='__main__':
    gui = TestGui()
    gui.run()