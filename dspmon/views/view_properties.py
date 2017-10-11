__author__ = 'bckong'


import random
#------------------------------------------
#  Table attributes
#------------------------------------------
id_panel_color=(0.15, 0.08, 0.08)
#table_color=(1, 0x88/255., 0)
#table_color=(random.random(), 1, 1)
table_color=(120./240., 1, 1)

#------------------------------------------
#  Table Text Attributes
#------------------------------------------
name_color="    [color=ffffff]{0:s}[/color]"
value_on_color="    [color=00ff00]{0:s}[/color]"
value_off_color="    [color=505050]{0:s}[/color]"




#---------------------------------------------------
#  Test kivy properties
#---------------------------------------------------
from kivy.properties import DictProperty
from kivy.event import EventDispatcher
class PropTest(EventDispatcher):
    features=DictProperty()

    def __init__(self, **kw):
        super(PropTest, self).__init__(**kw)

        self.features=kw.get('features', {})

        self.bind(features=self.on_change)

    def on_change(self, instance, value):
        print "chnages ", value
        print self.features




if __name__=='__main__':
    p=PropTest(features={'x':20, 'y':30})

    p2=PropTest()
    p2.features={'x':100, 'y':77}
    print p.features
    print p2.features
