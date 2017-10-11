__author__ = 'bxkong'

import random
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView

import table
import view_properties as view_prop


__all__=( 
    'ScrollTables',
)


#-------------------------------------
# ScrollTables interface
#   - tables content: list(dict, dict, ...),
#                     number of items in the list
#                     determine number of tables in 
#                     ScrollTables view
#   - table height: table heigh(single table)
#-------------------------------------
table_height=300


class ScrollTables(GridLayout):
    """
    the class contains 2 or more tables
    """

    def __init__(self, **kw):
        super(ScrollTables, self).__init__(**kw)
        self.padding=10
        self.spacing=3

        self.cols=1
        self.bind(minimum_height=self.setter('height'))

        self._tables=[]

        #------------------------------
        # get table contents & height
        #------------------------------
        contents=kw.get('contents')
        height=kw.get('table_height')


        # adding tables to the grid layout
        #color=(random.random(), 1., 1.)
        color=(120.0/240., 1., 1.)
        for props in contents:
            tbl=table.Table(contents=props, table_color=color)
            tbl.size_hint=(1, None)
            tbl.height=height
            self._tables.append(tbl)
            self.add_widget(tbl)


    def update(self, properties):
        for i, table in enumerate(self._tables):
            table.update(properties[i])




debug_contents=None

# Make the table layout scrollable
class Panel(ScrollView):
    """
    input: 
    """
    def __init__(self, **kw):
        super(Panel, self).__init__(**kw)
        self._layout = None

        # get parameters
        encoders=kw.get('contents', debug_contents)
        height=kw.get('table_height', table_height)

        layout=ScrollTables(contents=encoders,
                            table_height=height)
        layout.size_hint=(1, None)
        layout.height=self.height
        self._layout=layout
        self.add_widget(layout)


        #layout.bind(height=self.setter('height'))

    def update(self, props):
        self._layout.update(props)



#-------------------------------------------
#  Unit test
#-------------------------------------------

#  Test sample format
debug_contents = ( \
    {
        'id':'Transcoder-A',
        'enable':'on',
        'DDI Select':'0',
        'Mode':'HDMI',
        'Bits Per Color':'24',
        'Port Width':'N/A',
        'Sync Polarity':'High',
        'DDI Clock Selected 0':'0',
    },
    {
        'id':'Transcoder-B',
        'enable':'on',
        'DDI Select':'0',
        'Mode':'HDMI',
        'Bits Per Color':'24',
        'Port Width':'N/A',
        'Sync Polarity':'High',
        'DDI Clock Selected 0':'0',
    },
    {
        'id':'Transcoder-C',
        'enable':'on',
        'DDI Select':'0',
        'Mode':'HDMI',
        'Bits Per Color':'24',
        'Port Width':'N/A',
        'Sync Polarity':'High',
        'DDI Clock Selected 0':'0',
    },
    {
        'id':'Transcoder-D',
        'enable':'on',
        'DDI Select':'0',
        'Mode':'HDMI',
        'Bits Per Color':'24',
        'Port Width':'N/A',
        'Sync Polarity':'High',
        'DDI Clock Selected 0':'0',
    }
)



class UnitTest(App):
    def build(self):
        trans=Panel(table_height=table_height)

        return trans


if __name__ == '__main__':
    UnitTest().run()
