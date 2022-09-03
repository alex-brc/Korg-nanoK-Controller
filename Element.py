from __future__ import absolute_import, print_function, unicode_literals
import Live
from _Framework.InputControlElement import MIDI_CC_TYPE
from _Framework.ButtonElement import ButtonElement as ButtonElementBase
from _Framework.SliderElement import SliderElement as SliderElementBase
from _Framework.Skin import Skin
from _Framework.ButtonElement import Color

class Colors:
    class DefaultButton:
        On = Color(127)
        Off = Color(0)
        Disabled = Color(0)

    class Transport:
        PlayOn = Color(127)
        PlayOff = Color(0)

    class Automation:
        On = Color(127)
        Off = Color(0)

    class Mixer:
        MuteOn = Color(0)
        MuteOff = Color(1)
        SoloOn = Color(1)
        SoloOff = Color(0)

class Factory:

    @staticmethod   
    def create_matrix(factory, base_name, identifier_matrix, *a, **k):
        # Flat names for matrix elements, i.e. <base_name>_6 for element at 2,3
        name_factory = lambda index : base_name + '_%d' % index 
        
        buttons = [ [
            factory(name_factory(row * column), identifier, *a, **k) 
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
            skin=Skin(Colors.DefaultButton), 
            *a, **k)

class SliderElement(SliderElementBase):
    def __init__(self, name, code, *a, **k):
        super(SliderElement, self).__init__(
            name=name, 
            identifier=code, 
            channel=0, 
            msg_type=MIDI_CC_TYPE, 
            *a, **k)