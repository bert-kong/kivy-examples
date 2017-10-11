__author__ = 'bxkong'

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.screenmanager import (Screen, ScreenManager, FadeTransition)
from kivy.properties import ObjectProperty


class PipeScreen(Screen):

    button=ObjectProperty()

    def __init__(self, **kw):
        super(PipeScreen, self).__init__(**kw)

        self.name=kw.get('name', None)

        inter_layout=BoxLayout(orientation='vertical')
        self.add_widget(inter_layout)

        #-------------------------------------
        # anchor for transition button
        #-------------------------------------
        anchor=AnchorLayout()
        anchor.anchor_x='left'
        anchor.anchor_y='top'
        inter_layout.add_widget(anchor)

        btn=Button(text='Plane')
        btn.id='plane'
        btn.size_hint=(None, None)
        btn.size=(50, 30)
        self.button=btn
        anchor.add_widget(btn)




class CursorScreen(Screen):
    button=ObjectProperty()

    def __init__(self, **kw):
        super(CursorScreen, self).__init__(**kw)
        self.name='cursor'

        layout=BoxLayout()
        btn=Button(text='Cursor')
        btn.id='cursor'
        self.button=btn

        layout.add_widget(btn)
        self.add_widget(layout)



class View(ScreenManager):
    def __init__(self, **kw):
        super(View, self).__init__(**kw)

        self.transition=FadeTransition()
        self.plane=PlaneScreen()
        self.plane.button.bind(on_press=self.on_press_button)

        self.cursor=CursorScreen()
        self.cursor.button.bind(on_press=self.on_press_button)

        self.add_widget(self.plane)
        self.add_widget(self.cursor)

        self.current=self.plane.name

    def on_press_button(self, instance):
        print "-----> ", instance.id

        if instance.id=='plane':
            self.current='cursor'
            print "change to cursor"
        elif instance.id=='cursor':
            self.current='plane'
            print "change to plane"



class UnitTest(App):
    def build(self):
        view = View()

        return view


if __name__ == '__main__':
    UnitTest().run()
