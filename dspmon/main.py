__author__ = 'bckong'

import sys

from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.tabbedpanel import TabbedPanelItem
from kivy.uix.button import Button
from kivy.app import App


from dspmon.views import graphics, display
from dspmon.views import codecs
from dspmon.views import control
from dspmon.views import about
import ipccli


#-------------------------------------------
#  Control tab
#-------------------------------------------
display.debug=True

class AboutTab(TabbedPanelItem):

    def __init__(self, **kw):
        super(AboutTab, self).__init__(**kw)
        self.text='About'

	view=about.View()

        self.add_widget(view)



class ControlTab(TabbedPanelItem):

    def __init__(self, **kw):
        super(ControlTab, self).__init__(**kw)
        self.text='Control'

	ctrl=control.View()


        self.add_widget(ctrl)



#-------------------------------------------
#  Graphics
#-------------------------------------------
class GraphicsTab(TabbedPanelItem):

    def __init__(self, **kw):
        super(GraphicsTab, self).__init__(**kw)
        self.text='Graphics'

        view= graphics.View()
        self.add_widget(view)

#-------------------------------------------
#  Codec 
#-------------------------------------------
class CodecTab(TabbedPanelItem):

    def __init__(self, **kw):
        super(CodecTab, self).__init__(**kw)
        self.text='Codecs'

        view=codecs.View()

        self.add_widget(view)


class MainView(TabbedPanel):

    def __init__(self, **kw):
        super(MainView, self).__init__(**kw)
        self.do_default_tab=True
        self.tab_height=20

        #-----------------------------------------
        #  Display Tab
        #-----------------------------------------
        self.default_tab_text='Display'
        self.default_tab_content= display.View()

        #-----------------------------------------
        #  Graphics Tab
        #-----------------------------------------
        gfx_tab=GraphicsTab()
        self.add_widget(gfx_tab)

        #-----------------------------------------
        #  Codecs Tab
        #-----------------------------------------
        codec_tab=CodecTab()
        self.add_widget(codec_tab)

        #-----------------------------------------
        #  Control Tab
        #-----------------------------------------
        # TODO: contrl
        control_tab=ControlTab()
        self.add_widget(control_tab)

        #-----------------------------------------
        #  About Tab
        #-----------------------------------------
        # TODO: about
        about_tab=AboutTab()
        self.add_widget(about_tab)


class UnitTest(App):

    def build(self):
        self.title='DspMon'
        self._view=MainView()

        return self._view

    def on_start(self):
        print "start Dspmon"

    def on_stop(self):
        print "stop Dspmon"
        self._view.default_tab_content.close()



if __name__=='__main__':
    UnitTest().run()

