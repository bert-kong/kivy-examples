__author__ = 'bckong'

import os
import time
import threading
# -----------------------------------------
#   Kivi modules
# -----------------------------------------
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.app import App
from kivy.properties import BooleanProperty
from kivy.properties import NumericProperty
from kivy.properties import ObjectProperty
from kivy.clock import Clock



# -----------------------------------------
#  Display unit view panels
#  interface:
#       table.Panel(size_hint=(panel_size/width, 1.)
#       pipe.Panel(.9, 1.)
# -----------------------------------------
import dspmon.views.introduction as introduction
import dspmon.views.scrolltables as table
import dspmon.views.warning as warning
import dspmon.views.wait_warning as wait_warning
import dspmon.views.underdevelopment as under_dev
import dspmon.views.pysv_progressbar as wait_svpy

import sys

sys.path.append(r'C:\PythonSv\broxton\vjt\display\sv')

# -----------------------------------------
# Display DataPort
#     dataport=DataPort('pipe')
#     dataport.update():[return_code, msg|{}]
#          [0, {}] - return subunit properties
#          [1, msg] - return error messages
# -----------------------------------------

import_pydsp_error = False
import_pydsp_error_msg = """
[color=FF0000]Please update PytyonSV/vjt/display/sv/pydsp and restart the dspmon[/color]
"""

try:
    import pydsp.monitor.model.dataport as dataport

except ImportError, err:
    message = "display.py --->  %s " % (str(err),)
    import_pydsp_error = True

__all__ = ( \
    'View',
    'debug',
    )

im_dir = r'C:\PythonSv\broxton\vjt\display\sv\pydsp\monitor\res'
im_file = os.path.join(im_dir, 'button_red.png')


# ------------------------------------------
#  Reading Thread 
# ------------------------------------------
class ReadingThread(threading.Thread):
    def __init__(self, obj, name="ReadingReadThead"):
        super(ReadingThread, self).__init__(name=name)
        self._obj = obj

        # TODO: change False --> True for releasing
        self._debug = False
        #self._debug = True

    def run(self):
        """
        Reading HW registers
        """

        #time.sleep(4)
        if self._obj.data:
            self._obj._return_code, self._obj._return_data = self._obj.data.update(debug=self._debug)
            self._obj.reading_data_done = True
            self._obj._spin_msg = False

        return


# ------------------------------------------
#  Global Variables
# ------------------------------------------
start_python_session_done = False
dspmon_idle = True


class UpdateButton(ToggleButton):
    update = NumericProperty(0)
    debug = BooleanProperty(False)
    view = ObjectProperty()
    data = ObjectProperty()

    reading_data_done = BooleanProperty(False)

    def __init__(self, **kw):
        super(UpdateButton, self).__init__(**kw)
        self.group='display-control-button'

        # the name of button = text
        self.name=self.text

        self.markup=True

        # state=down image
        self.background_down=os.path.join(im_dir, 'btn_toggle_down.png')

        self._spin_msg = False

        self._return_data = None
        self._return_code = 1

        self.bind(state=self.on_state_change)

        # -------------------------------------
        # display sub-unit view & properties
        # -------------------------------------
        self.view = kw.get('view', None)
        self.data = kw.get('data', None)

        self.warning = warning.View()
        self.wait_warning=wait_warning.View()

        # -------------------------------------
        # button configuration/attributes
        # -------------------------------------
        self._im = Image(source=im_file)
        #self._im = wait_svpy.ProgressBarAnimation()
        #self._im.bind(pos=self.on_pos_size_change)
        #self._im.bind(size=self.on_pos_size_change)

        self.bind(pos=self.on_pos_size_change)
        self.bind(size=self.on_pos_size_change)

        # -------------------------------------
        #  reading done event
        # -------------------------------------
        self.bind(reading_data_done=self.update_view)


    def on_state_change(self, instance, value):
        if value=='normal':
            #self.opacity=1.0
            self.text=self.name
        elif value=='down':
            #self.opacity=.2
            self.text="[b][color=00FF00]%s[/color][/b]" % (self.name, )

    def reading_data(self):
        self.add_widget(self._im)

        # create thread to read HW data
        self.reading_data_done = False
        read_data_thread = ReadingThread(self)
        read_data_thread.start()

        global start_python_session_done
        if start_python_session_done == False:
            #start_python_session_done = True
            self._spin_msg = True
            spin_msg = threading.Thread(target=self.cmd_line_msg)
            spin_msg.start()

            self.wait_warning.open()
            self.wait_warning.start()

    def release_button(self):
        """
        remove the button image
        """
        global dspmon_idle
        dspmon_idle = True

        self.state='down'


    def update_view(self, instance, value):
        """
        using the return data to update table/view
        """

        if self.reading_data_done is False:
            return


        # return off reading waiting image/message
        global start_python_session_done
        if start_python_session_done==False:
            self.wait_warning.stop()
            self.wait_warning.dismiss()
            start_python_session_done = True

	
        self.remove_widget(self._im)

        print "reading thread was done!!!"
        # -------------------------------------
        #  check return
        # -------------------------------------
        if self.data:
            # reading error
            print "dspmon return code ---> ", self._return_code
            if self._return_code != 0:
                print "dspmon error msg ---> ", self._return_data

                self.warning.message.text = self._return_data if self._return_data else "Unknow error"
                self.warning.open()
                return


            # -----------------------------
            #  normal return
            #  update view with HW data
            # -----------------------------
            if self.view:
                self.view.update(self._return_data)

    def on_pos_size_change(self, instance, value):
        # make image.center=button.center
        self._im.center = self.center

    def cmd_line_msg(self):
        time.sleep(8)
        spin_code = 1
        print "\n\n\n"
        while self._spin_msg:
            if spin_code == 1:
                print "\rStarting Python SV Session, Please wait -  ",
            elif spin_code == 2:
                print "\rStarting Python SV Session, Please wait \\ ",
            elif spin_code == 3:
                print "\rStarting Python SV Session, Please wait |",
            elif spin_code == 4:
                print "\rStarting Python SV Session, Please wait -",
            elif spin_code == 5:
                print "\rStarting Python SV Session, Please wait /",
            else:
                spin_code = 0

            spin_code += 1
            time.sleep(.2)


# ------------------------------------------
#  Main View
# ------------------------------------------
class View(BoxLayout):
    """
    control panel
    information panel
    """

    _current_view = ObjectProperty()
    dataport = ObjectProperty()

    def __init__(self, **kw):
        super(View, self).__init__(**kw)

        self.orientation = 'horizontal'

        # ---------------------------------------
        # check pydsp update & display message
        # ---------------------------------------
        if import_pydsp_error:
            warn = Label()
            warn.text = import_pydsp_error_msg
            warn.markup = True
            warn.font_size = 20
            self.add_widget(warn)
            return

        # -------------------------------------------------
        # Data Port the client/server socket
        # -------------------------------------------------
        self.dataport = dataport.DataPort

        # -------------------------------------------------
        # ratio btw control panel & display views
        # -------------------------------------------------
        self._ratio = .9

        # --------------------------------
        #  Display views
        # --------------------------------
        self._display_view = None
        self._pipe_view = None
        self._transcoder_view = None
        self._mipi_view = None
        self._port_view = None
        self._audio_view = None
        self._panel_view = None
        self._engine_view = None



        # -------------------------------------------------
        # Control Panel
        #   - pipe: Button(text='Pipe', bind=callback)
        #   - transcoder
        #   - port
        #   ...
        # -------------------------------------------------
        control_panel_view = BoxLayout(orientation='vertical')
        control_panel_view.size_hint = (0.2, 1.)
        self._control_panel_view = control_panel_view

        # -------------------------------------------------
        # configure display views (data, view and control)
        # -------------------------------------------------
        self.config_display_block_view()
        self.config_engine_view()
        self.config_pipe_view()
        self.config_transcoder_view()
        self.config_port_view()
        self.config_mipi_view()
        self.config_audio_view()
        self.config_panel_view()


        # add to the top view tree
        self._current_view = self._display_view
        self.add_widget(self._control_panel_view)
        self.add_widget(self._current_view)

    def config_display_block_view(self):
        self._display_view = introduction.Panel()
        self._display_view.size_hint = (.8, 1.)

        self._current_view = self._display_view

        # button control
        button_display = UpdateButton(text="Display Diagram")
        button_display.bind(on_press=self.on_press_display_view_button)

        self._control_panel_view.add_widget(button_display)

    def config_pipe_view(self):
        """
        set 1) Data Port & View
            2) button control the port & view
        """

        #  data port, view
        pipe_data = dataport.DataPort('pipe')
        ret_code, data = pipe_data.update(debug=True)
        self._pipe_view = table.Panel(size_hint=(self._ratio, 1.),
                                      contents=data)

        #  button control
        button_pipe = UpdateButton(text="Pipe",
                                   data=pipe_data,
                                   view=self._pipe_view)

        #  bind
        button_pipe.bind(on_press=self.on_press_view_button)
        button_pipe.bind(on_release=self.on_release_pipe_view_button)

        self._control_panel_view.add_widget(button_pipe)

    def config_transcoder_view(self):
        """
        set 1) Data Port & View
            2) button control the port & view
            3) binding
        """

        #  Transcoder dataport & view
        trans_data = dataport.DataPort('transcoder')
        ret_code, data = trans_data.update(debug=True)
        self._transcoder_view = table.Panel(size_hint=(self._ratio, 1.), contents=data)

        #  button
        button_transcoder = UpdateButton(text='Transcoder',
                                         data=trans_data,
                                         view=self._transcoder_view)

        #  bind
        button_transcoder.bind(on_press=self.on_press_view_button)
        button_transcoder.bind(on_release=self.on_release_transcoder_button)

        self._control_panel_view.add_widget(button_transcoder)

    def config_port_view(self):
        """
        set 1) Data Port & View
            2) button control the port & view
            3) binding
        """

        #  Transcoder dataport & view
        port_data = dataport.DataPort('port')
        ret_code, data = port_data.update(debug=True)
        self._port_view = table.Panel(size_hint=(self._ratio, 1.), contents=data)

        button_port = UpdateButton(text='Port',
                                   data=port_data,
                                   view=self._port_view)

        button_port.bind(on_press=self.on_press_view_button)
        button_port.bind(on_release=self.on_release_port_button)
        self._control_panel_view.add_widget(button_port)

    def config_engine_view(self):
        """
        set 1) Data Port & View
            2) button control the port & view
            3) binding
        """

        engine_data = dataport.DataPort('engine')
        ret_code, data = engine_data.update(debug=True)
        self._engine_view = table.Panel(size_hint=(self._ratio, 1.), contents=data)

        button_engine = UpdateButton(text='Display Engine',
                                     data=engine_data,
                                     view=self._engine_view)

        button_engine.bind(on_press=self.on_press_view_button)
        button_engine.bind(on_release=self.on_release_engine_button)
        self._control_panel_view.add_widget(button_engine)

    def config_mipi_view(self):
        """
        set 1) Data Port & View
            2) button control the port & view
            3) binding
        """

        data_port = dataport.DataPort('mipi')
        ret_code, data = data_port.update(debug=True)
        self._mipi_view = table.Panel(size_hint=(self._ratio, 1.), contents=data)

        button = UpdateButton(text='MIPI',
                              data=data_port,
                              view=self._mipi_view)

        button.bind(on_press=self.on_press_view_button)
        button.bind(on_release=self.on_release_mipi_button)
        self._control_panel_view.add_widget(button)

    def config_panel_view(self):
        self._panel_view = under_dev.Panel()

        button = Button(text='Panel')
        button.bind(on_press=self.on_press_panel_button)
        self._control_panel_view.add_widget(button)


    def config_audio_view(self):
        self._audio_view = under_dev.Panel()

        button = Button(text='Audio')
        button.bind(on_press=self.on_press_audio_button)
        self._control_panel_view.add_widget(button)

    # ------------------------------------------
    # callbacks for control button
    # ------------------------------------------
    def on_press_display_view_button(self, instance):
        # 3) display the widget
        self.remove_widget(self._current_view)
        self.add_widget(self._display_view)
        self._current_view = self._display_view

    # ------------------------------------------
    def on_press_view_button(self, instance):
        global dspmon_idle

        if dspmon_idle == False:
            return

        dspmon_idle = False
        instance.reading_data()

    # ------------------------------------------
    def on_release_pipe_view_button(self, instance):
        instance.release_button()

        # remove old view & add the requested view
        self.remove_widget(self._current_view)
        self.add_widget(self._pipe_view)
        self._current_view = self._pipe_view

    # ------------------------------------------
    def on_release_transcoder_button(self, instance):
        instance.release_button()

        # remove old view & add the requested view
        self.remove_widget(self._current_view)
        self.add_widget(self._transcoder_view)
        self._current_view = self._transcoder_view

    def on_release_port_button(self, instance):
        instance.release_button()

        # 2) display pipe widget
        self.remove_widget(self._current_view)
        self.add_widget(self._port_view)
        self._current_view = self._port_view

    def on_release_engine_button(self, instance):
        instance.release_button()

        # change to PM view
        self.remove_widget(self._current_view)
        self.add_widget(self._engine_view)
        self._current_view = self._engine_view

    def on_release_mipi_button(self, instance):
        instance.release_button()

        # change to PM view
        self.remove_widget(self._current_view)
        self.add_widget(self._mipi_view)
        self._current_view = self._mipi_view

    def on_press_panel_button(self, instance):
        self.remove_widget(self._current_view)
        self.add_widget(self._panel_view)
        self._current_view = self._panel_view

    def on_press_audio_button(self, instance):
        self.remove_widget(self._current_view)
        self.add_widget(self._audio_view)
        self._current_view = self._audio_view

    #def on_press_underdevelopment_button(self, instance):
    #    # 3) display panel widget
    #    self.remove_widget(self._current_view)
    #    self.add_widget(self._panel_view)
    #    self._current_view = self._panel_view

    def close(self):
        if self.dataport:
            self.dataport.close()


# --------------------------------------
# Unit Test
# --------------------------------------
class MainApp(App):
    def build(self):
        self.title = 'BXT/BXT-P'

        ui = View()

        return ui


if __name__ == '__main__':
    MainApp().run()
