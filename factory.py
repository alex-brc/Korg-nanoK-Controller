from __future__ import absolute_import, print_function, unicode_literals
from io import DEFAULT_BUFFER_SIZE
import Live
from _Framework.InputControlElement import MIDI_CC_TYPE
from _Framework.ButtonElement import ButtonElement
from _Framework.EncoderElement import EncoderElement
from _Framework.SliderElement import SliderElement
from _Framework.ButtonMatrixElement import ButtonMatrixElement
from _Framework.ComboElement import ComboElement
from _Framework.Skin import Skin
from _Framework.ButtonElement import Color

class Defaults:

    class DefaultButton:
        On = Color(127)
        Off = Color(63)
        Disabled = Color(0)

class SkinFactory:

    @staticmethod
    def make_default_skin():
        return Skin(Defaults)


class Factory:
    
    DEFAULT_BUTTON_SKIN = Skin(Defaults)

    @staticmethod
    def make_button(name, cc, *a, **k):
        return ButtonElement(True, MIDI_CC_TYPE, 0, cc, name=name, skin=Factory.DEFAULT_BUTTON_SKIN, *a, **k)

    @staticmethod
    def make_toggle(name, cc, *a, **k):
        return ButtonElement(False, MIDI_CC_TYPE, 0, cc, name=name, skin=Factory.DEFAULT_BUTTON_SKIN, *a, **k)

    @staticmethod
    def make_slider(name, cc, *a, **k):
        return SliderElement(MIDI_CC_TYPE, 0, cc, name=name, *a, **k)

    @staticmethod
    def make_encoder(name, cc, *a, **k):
        return EncoderElement(MIDI_CC_TYPE, 0, cc, Live.MidiMap.MapMode.absolute, name=name, *a, **k)

    @staticmethod
    def make_matrix(name, element_factory, cc, *a, **k):
        def one_dimensional_name(base_name, x, _y):
            return u'%s[%d]' % (base_name, x)

        def two_dimensional_name(base_name, x, y):
            return u'%s[%d,%d]' % (base_name, x, y)

        name_factory = two_dimensional_name if len(cc) > 1 else one_dimensional_name
        
        elements = []
        for row, identifiers in enumerate(cc):
            elements_in_row = []
            for column, identifier in enumerate(identifiers):
                elements_in_row.append(element_factory(name_factory(name, column, row), identifier, *a, **k))
            elements.append(elements_in_row)

        return elements

    @staticmethod
    def make_shifted_element(element, shifter):
        return ComboElement(element, modifiers=[shifter])

    @staticmethod
    def make_shifted_matrix(element_matrix, shifter):
        elements = []
        for row in element_matrix:
            elements_in_row = []
            for element in row:
                elements_in_row.append(ComboElement(element, modifiers=[shifter]))
            elements.append(elements_in_row)

        return elements
