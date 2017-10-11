__author__ = 'bckong'

from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App


class View(Popup):

    message=ObjectProperty()

    def __init__(self, **kw):
        super(View, self).__init__(**kw)

        self.title='Warning'
        self.title_color=[1, 1, 1, 1]
        self.title_size='16sp'
        self.size_hint=(.4, .4)

        content=BoxLayout(orientation='vertical')
        content.padding=10
        label=Label(text='Lauterbach timeout error!')
        label.bind(size=self.on_change_size)
        label.halign='left'
        label.valign='top'
        self.message=label

        button=Button(text='close')
        button.size_hint=(0.3, 0.3)
        button.pos_hint={'center_x':0.5, 'center_y':0.5}
        button.bind(on_press=self.on_press_button)

        content.add_widget(label)
        content.add_widget(button)
        self.content=content

    def on_press_button(self, instnace):
        self.dismiss()


    def on_change_size(self, instance, value):
        self.message.text_size=self.message.size

#------------------------------------------
#  Unit Test
#------------------------------------------
class UnitTest(App):

    def build(self):

        view=Widget()

        btn=Button(text="show warnign")
        btn.bind(on_press=self.on_press_button)

        warning=View()
        self._warning=warning

        view.add_widget(btn)

        return view

    def on_press_button(self, instance):
        print "open popup"
        self._warning.message.text="Syntax errors, also known as parsing errors, are perhaps the most common kind of complaint you get while you are still learning python"
        self._warning.open()

if __name__=='__main__':
    UnitTest().run()
