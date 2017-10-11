__author__ = 'bxkong'

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
import kivy.graphics.context_instructions as ctx
import kivy.graphics.vertex_instructions as vtx

import view_properties as prop


__all__ = (
    'Table',
    'TablePanel',
    'HeaderPanel',
)


"""
public object table in the table.py module
    -Table
        create 2 panels, ID panel + table with entries
        populated with the input contents

        id:unit name --> HeaderPanel.text
        HeaderPanel.text=contents['id']

        for the table interface, id:unit & enable:on/off are must 
        contents: 
        { 
            'id':'unit name'
            'enable':'on/off'
            'xxx':'yyy'
            ...
        }


    -TablePanel
        only create a table with entries populated with contents

        for the TablePanel interface, enable:on/off is must 
        contents: 
        { 
            'enable':'on/off'
            'xx':'yy'
            ...
        }

    -HeaderPanel
        only create a table with entries populated with contents
"""


class Cell(Label):
    """
    table cell
    """

    def __init__(self, **kw):
        super(Cell, self).__init__(**kw)
        self.markup = True
        self.halign = 'left'
        self.valign = 'middle'
        self.size_hint = (.5, 1.)

        r, g, b = kw.get('color', prop.table_color)

        color = ctx.Color(r, g, b, mode='hsv')
        rect = vtx.Line(rectangle=self.rectangle(), width=.5)
        self._rect = rect

        self.bind(pos=self.on_pos_size_change,
                  size=self.on_pos_size_change)

        self.canvas.add(color)
        self.canvas.add(rect)

        # color = ctx.Color(1, 1, 1)
        # self.canvas.after.add(color)

    def rectangle(self):
        w, h = self.size
        x, y = self.pos

        # w-=2; h-=2; x+=1; y+=1

        return (x, y, w, h)

    def on_pos_size_change(self, instance, value):
        self._rect.rectangle = self.rectangle()
        self.text_size = self.size


class Entry(BoxLayout):
    """
    Entry : name | value cell
    """

    def __init__(self, **kw):
        super(Entry, self).__init__(**kw)
        self.orientation = 'horizontal'
        self._value_cell=None
        self._color_off = False

        # -------------------------------------------
        # get parameters
        # -------------------------------------------
        color = kw.get('color', prop.table_color)
        font_size = kw.get('font_size', 10)

        attr, value = kw.get('item', ('name', 'value'))

        attr_cell = Cell(color=color, text=attr, font_size=font_size)
        value_cell = Cell(color=color, text=value, font_size=font_size)
        self._value_cell=value_cell

        self.add_widget(attr_cell)
        self.add_widget(value_cell)

    
    @property
    def prop(self):
        return self._value_cell


    @staticmethod
    def entry_color(v, unit_off=False):

        if unit_off or v=='off':
            return prop.value_off_color.format(v)

        return prop.value_on_color.format(v)



#-----------------------------------
#  Table outline
#-----------------------------------
class TableFrame(BoxLayout):
    """
    table frame/outline
    """

    def __init__(self, **kw):
        super(TableFrame, self).__init__(**kw)

        r, g, b = kw.get('color', prop.table_color)

        x, y, w, h=self.rectangle()
        with self.canvas:
            ctx.Color(r, g, b, mode='hsv')
            self._outline=vtx.Line(rectangle=(x, y, w, h), width=.5)

        self.bind(pos=self.on_pos_size_change,
                  size=self.on_pos_size_change)


    def on_pos_size_change(self, instance, value):
        self._outline.rectangle = self.rectangle()


    def rectangle(self):
        x, y = self.pos
        w, h = self.size

        x += 1
        y += 1
        w -= 2
        h -= 2

        return x, y, w, h


class TablePanel(TableFrame):
    """
    TablePanel (contents={k:v})
    contents format
        {
            'properties:value,
            ...
        }
    """

    def __init__(self, **kw):
        super(TablePanel, self).__init__(**kw)
        self.orientation = 'vertical'

        # save table entries(label.txt) for the table
        # update
        self._entries={}

        # ---------------------------------------------
        #  get parameters
        # ---------------------------------------------
        color = kw.get('color', prop.table_color)
        contents = kw.get('contents')

        #-------------------------------------------
        # every sub-unit has a enable field
        # if the unit is disabled, then color 
        # is dimmed
        #-------------------------------------------
        off=True if contents['enable']=='off' else False

        # populate the table entries
        for k, v in contents.items():
            name = prop.name_color.format(k)

            value = Entry.entry_color(v, unit_off=off)

            #------------------------
            #  capitalize text
            #------------------------
            name.title()
            value.title()
            entry = Entry(color=color,
                          font_size=17,
                          item=(name, value))

            # save the label for text change
            self._entries[k]=entry.prop
            self.add_widget(entry)


    def update(self, properties):
        """
        update the table entrie value
        propertes = 
            {
                'id':'unit name',
                'xx':'yy'
                ...
            }
        """

        off=True if properties['enable']=='off' else False
        for k, v in properties.items():
            self._entries[k].text=Entry.entry_color(v, unit_off=off)



class HeaderPanel(Label):
    def __init__(self, **kw):
        super(HeaderPanel, self).__init__(**kw)
        self.markup = True

        # header panel color
        r, g, b = kw.get('color', prop.id_panel_color)

        # get the ID panel's position & size
        pos, size = self.rectangle()

        with self.canvas.before:
            ctx.Color(r, g, b, mode='rgb')
            self._rect=vtx.Rectangle(pos=pos, size=size)

        self.bind(pos=self.on_pos_size_change,
                  size=self.on_pos_size_change)

    def rectangle(self):
        """
        return the widget/label position & size
        """
        pos = self.pos
        size = self.size

        return (pos, size)

    def on_pos_size_change(self, instance, value):
        pos, size = self.rectangle()

        self._rect.pos = pos
        self._rect.size = size


class Table(BoxLayout):
    """
    input: ID:'Unit-A'
           contents format, id(lower case) is a must
            {
               id : uint name,
               enable : on/off
               property:value
               ...
            }

           height:size hint=(1, None)

    Table properties:
        cell & id panel color etc. are in view_properies.py module
    """

    def __init__(self, **kw):
        super(Table, self).__init__(**kw)
        self.orientation = 'vertical'

        self._table = None
        self._header = None

        # -----------------------------------------
        # get parameters - table contents
        # -----------------------------------------
        attribs = kw.get('contents', None)
        color=kw.get('table_color', prop.table_color)
        # print "------------------  attribs ", attribs

        # get ID & remove it
        ID = attribs.pop('id')
        # print "------------------  ID ", ID

        # -----------------------------------------
        # ID panel
        # -----------------------------------------
        head_text="[color=ffffff]%s[/color]" % (ID,)
        header = HeaderPanel(color=prop.id_panel_color,
                             text=head_text,
                             size_hint=(1, None))

        header.height = 50.0

        # Text alignment & size
        header.halign = 'center'
        header.valign = 'middle'
        header.font_size=20

        header.bind(size=self.on_change_size)

        self._header = header

        # -----------------------------------------
        #  contents panel: cell(key, value)
        # -----------------------------------------
        panel = TablePanel(color=color,
                           contents=attribs,
                           size_hint=(1, 1))

        self._table=panel
        self.add_widget(header)
        self.add_widget(panel)


    def on_change_size(self, instance, value):
        """
        set label size == text size
        :param instance:
        :param value:
        :return:
        """
        pass
        # self._id_panel.text_size = (value[0], None)
        # self._id_panel.texture_size = (None, value[1])
        # print self._id_panel.texture_size

        # self._id_panel.texture_size=value


    def update(self, properties):
        """
        update the table entrie value
        propertes = 
            {
                'id':'unit name',
                'xx':'yy'
                ...
            }
        """
        self._table.update(properties)

# ---------------------------------------------------
#   Unit Test
#   id & enable are must fields for the table
# ---------------------------------------------------
prop_table3 = {
    'id': 'Plane-A',
    'enable': 'on',
    'property 0': 'on',
    'property 1': 'off',
    'alpha mode': 'off',
    'pipe csc enable': 'off',
    'plane rotation': '90 degree',
    'feature 0': 'feature',
    'feature 1': 'feature',
}

prop_table = prop_table3


class UnitTest(App):
    def build(self):
        table = Table(contents=prop_table)
        table.size_hint = (1., None)
        table.height = 300.0

        return table


if __name__ == '__main__':
    UnitTest().run()
