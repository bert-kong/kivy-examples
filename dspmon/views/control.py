__author__ = 'bckong'

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.properties import DictProperty

import_pydsp_error=None

try:
    import pydsp.monitor.model.dataport as dataport

except ImportError, err:
    message = "display.py --->  %s " % (str(err),)
    import_pydsp_error = True

class ReloadButton(Button):

    def __init__(self, **kw):
        super(ReloadButton, self).__init__(**kw)
        self._dataport=None


class View(GridLayout):

    btn_id=DictProperty({ \
                            # (id, text)
                            (0, 0) : [None, '    Start PythonSV Session'],
                            (1, 0) : [None, '    reload engine module'],
                            (2, 0) : [None, '    reload pipe module'],
                            (3, 0) : [None, '    reload transcoder module'],
                            (4, 0) : [None, '    reload port module'],
                            (5, 0) : [None, '    reload MIPI module'],
                            (6, 0) : [None, '    '],
                            (0, 1) : [None, '    '],
                            (1, 1) : [None, '    '],
                            (2, 1) : [None, '    '],
                            (3, 1) : [None, '    '],
                            (4, 1) : [None, '    '],
                            (5, 1) : [None, '    '],
                            (6, 1) : [None, '    '],
	                     })

    def __init__(self, **kw):
        super(View, self).__init__(**kw)

        self.padding=2
        self.spacing=1

        self.cols=2
        self.rows=7

        for row in range(self.rows):
            for col in range(self.cols):
                btn=ReloadButton()
                btn.text=self.btn_id[(row, col)][1]
                btn.bind(size=self.on_button_size_change)
                btn.bind(on_press=self.on_button_pressed)
                btn.font_size=26
                btn.halign='left'
                btn.valign='middle'
                btn.markup=True
                self.btn_id[(row, col)][0]=btn
                self.add_widget(btn)


        self.btn_id[(0, 0)][0]._dataport=None
        self.btn_id[(1, 0)][0]._dataport=dataport.DataPort('engine')
        self.btn_id[(2, 0)][0]._dataport=dataport.DataPort('pipe')
        self.btn_id[(3, 0)][0]._dataport=dataport.DataPort('transcoder')
        self.btn_id[(4, 0)][0]._dataport=dataport.DataPort('port')
        self.btn_id[(5, 0)][0]._dataport=dataport.DataPort('mipi')


    def on_button_size_change(self, instance, value):
        instance.text_size=instance.size

    def on_button_pressed(self, instance):
        if instance._dataport:
            #instance._dataport.reload(debug=True)
            instance._dataport.reload()


class UnitTest(App):
    def build(self):
        view = View()

        return view


if __name__ == '__main__':
    UnitTest().run()
