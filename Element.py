from __future__ import absolute_import, print_function, unicode_literals
import logging
from subprocess import call
import Live
from _Framework.InputControlElement import InputControlElement, MIDI_CC_TYPE, MIDI_SYSEX_TYPE
from _Framework.ButtonElement import ButtonElement as ButtonElementBase
from _Framework.SliderElement import SliderElement as SliderElementBase
from _Framework.Util import nop, const
from _Framework.Skin import Skin
from .Colors import Colors
from .Sysex import Sysex, _SYSEX_START
logger = logging.getLogger(__name__)

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


class SysexButtonElement(InputControlElement):
    def __init__(self, name, sysex_event_bytes, sysex_command_bytes=None, translate_value=const, *a, **k):
        super(SysexButtonElement, self).__init__(
            name=name, 
            sysex_identifier=_SYSEX_START + Sysex.MANUFACTURER_BYTES + sysex_event_bytes, 
            msg_type=MIDI_SYSEX_TYPE, 
            *a, **k)
        self._sysex_command_bytes = sysex_command_bytes
        self._translate_value = translate_value
    
    def send_value(self, value):
        if self._sysex_command_bytes is not None:
            self.send_midi(Sysex.Message(self._sysex_command_bytes, value).bytes)
        
    def receive_value(self, value):
        value = self._translate_value(value)
        self.notify_value(value)


class AnimatedButtonElement(ButtonElement):
    def __init__(self, name, code, *a, **k):
        super(AnimatedButtonElement, self).__init__(name, code, *a, **k)
        self._animation = None

    def set_light(self, value):
        self._stop_animation()
        super(AnimatedButtonElement, self).set_light(value)
    
    def turn_off(self):
        self._stop_animation()
        super(AnimatedButtonElement, self).turn_off()
    
    def _stop_animation(self):
        if self._animation is not None:
            self._animation.kill()
            self._animation = None

class SliderElement(SliderElementBase):
    def __init__(self, name, code, *a, **k):
        super(SliderElement, self).__init__(
            name=name, 
            identifier=code, 
            channel=0, 
            msg_type=MIDI_CC_TYPE, 
            *a, **k)


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