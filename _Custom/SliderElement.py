from __future__ import absolute_import, print_function, unicode_literals
import logging
from _Framework.InputControlElement import MIDI_CC_TYPE
from _Framework.SliderElement import SliderElement as SliderElementBase

class SliderElement(SliderElementBase):
    def __init__(self, name, code, *a, **k):
        super(SliderElement, self).__init__(
            name=name, 
            identifier=code, 
            channel=0, 
            msg_type=MIDI_CC_TYPE, 
            *a, **k)