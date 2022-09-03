from __future__ import absolute_import, print_function, unicode_literals
import logging
from _Framework.InputControlElement import MIDI_CC_TYPE
from _Framework.ButtonElement import ButtonElement as ButtonElementBase
from _Framework.SliderElement import SliderElement as SliderElementBase
from _Framework.Skin import Skin
from _Framework.ButtonElement import Color
from _Framework.TransportComponent import TransportComponent
logger = logging.getLogger(__name__)

class Colors:
    class Button:
        # Standard button colors
        On = Color(127)
        Off = Color(0)

        # Button colors in session mode; standard names
        class Session:
            ClipTriggeredPlay = Color(127)      # Trigger to start
            ClipTriggeredRecord = Color(127)    # Triggered to record
            ClipStopped = Color(127)            # Clip exists but is stopped
            ClipStarted = Color(127)            # Clip is currently playing 
            ClipRecording = Color(127)          # Clip is currently recording
            RecordButton = Color(0)             # Clip slot is ready to be recorded into (slot with circle))
            # turn_off()                        # Clip does not exist in slot and cannot be recorded into (slot with square)

class Factory:

    @staticmethod   
    def create_matrix(factory, base_name, identifier_matrix, *a, **k):
        # Flat names for matrix elements, i.e. <base_name>_6 for element at 2,3
        name_factory = lambda index : base_name + '_%d_%d' % (index[0], index[1])

        buttons = [ [
            factory(name_factory((row, column)), identifier, *a, **k) 
            for column, identifier in enumerate(identifier_row) ] 
            for row, identifier_row in enumerate(identifier_matrix) ]

        return buttons

class ButtonElement(ButtonElementBase):
    def __init__(self, name, code, *a, **k):
        super(ButtonElement, self).__init__(
            name=name, 
            identifier=code, 
            is_momentary=True, 
            channel=0, 
            msg_type=MIDI_CC_TYPE, 
            skin=Skin(Colors.Button), 
            *a, **k)

class StopButtonElement(ButtonElement):
    def set_transport(self, transport):
        self._transport = transport
    
    # Turn on while song is stopped
    def set_light(self, value):
        if self._transport.song().is_playing == False:
            self._set_skin_light('On')
        else: 
            self._set_skin_light('Off')

class SessionButtonElement(ButtonElement):
    def set_light(self, value):
        logger.info('Lit button ' + self.name + ' with value: ' + str(value))
        self._set_skin_light(value)

class SliderElement(SliderElementBase):
    def __init__(self, name, code, *a, **k):
        super(SliderElement, self).__init__(
            name=name, 
            identifier=code, 
            channel=0, 
            msg_type=MIDI_CC_TYPE, 
            *a, **k)