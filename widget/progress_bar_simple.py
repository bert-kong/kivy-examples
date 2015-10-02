__author__ = 'bckong'


from kivy.app import App
from kivy.uix.progressbar import ProgressBar
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.clock import Clock

class View(BoxLayout):

    def __init__(self, **kw):
        super(View, self).__init__(**kw)
        self.orientation='vertical'
        self._do_update=False

        progress=ProgressBar()
        progress.size_hint=(1., None)
        progress.height=3
        self._progress=progress

        self.add_widget(progress)

        btn_0=Button(text='Pipe')
        btn_0.bind(on_press=self.on_press_pipe)
        self.add_widget(btn_0)

        btn_1=Button(text='Transcoder')
        btn_1.bind(on_press=self.on_press_transcoder)
        self.add_widget(btn_1)



    def update(self, dt):
        if self._do_update==False:
            return

        self._progress.value+=1

        if self._progress.value==self._progress.max:
            self._progress.value=0
            self._do_update=False
            return


    def on_press_pipe(self, value):
        self._do_update=True

    def on_press_transcoder(self, value):
        self._do_update=True



class UnitTest(App):

    def build(self):

        view=View()

        Clock.schedule_interval(view.update, 1./10.)

        return view




if __name__=='__main__':
    UnitTest().run()
