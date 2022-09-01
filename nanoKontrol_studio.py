from __future__ import absolute_import, print_function, unicode_literals
from _Framework.ControlSurface import ControlSurface
from _Framework.MidiMap import make_encoder, make_slider, MidiMap as MidiMapBase
from _Framework.InputControlElement import MIDI_CC_TYPE
from _Framework.ButtonElement import ButtonElement
from _Framework.Layer import Layer
from _Framework.TransportComponent import TransportComponent
from _Framework.MixerComponent import MixerComponent

# Track controls
FADERS = [2, 3, 4, 5, 6, 8, 9, 12]
KNOBS = [13, 14, 15, 16, 17, 18, 19, 20]
MUTE_BUTTONS = [21, 22, 23, 24, 25, 26, 27, 28]
SOLO_BUTTONS = [29, 30, 31, 33, 34, 35, 36, 37]
REC_BUTTONS = [38, 39, 40, 41, 42, 43, 44, 45]
SELECT_BUTTONS = [46, 47, 48, 49, 56, 51, 52, 53]

# Jog Wheel
JOG_SIGN_MAGNITUTE = 82
JOG_CLOCKWISE = 83
JOG_INCREMENT = 83
JOG_C_CLOCKWISE = 85
JOG_DECREMENT = 85
JOG_CONTINUOUS = 86

# Transport controls
CYCLE = 54
MARKET_SET = 55
MARKER_LEFT = 56
MARKER_RIGHT = 57
TRANSPORT_REWIND = 58
TRANSPORT_FORWARD = 59
TRACK_LEFT = 60
TRACK_RIGHT = 61
TRANSPORT_RETURN_TO_ZERO = 62
TRANSPORT_STOP = 63
TRANSPORT_PLAY = 80
TRANSPORT_RECORD = 81

class MidiMap(MidiMapBase):

    def __init__(self, *a, **k):
        super(MidiMap, self).__init__(*a, **k)
        
        # Map Transport controls
        self.add_momentary_button(u'Stop', TRANSPORT_STOP)
        self.add_momentary_button(u'Play', TRANSPORT_PLAY)
        self.add_momentary_button(u'Record', TRANSPORT_RECORD)
        self.add_momentary_button(u'Forward', TRANSPORT_FORWARD)
        self.add_momentary_button(u'Backward', TRANSPORT_REWIND)
        self.add_momentary_button(u'Reset', TRANSPORT_RETURN_TO_ZERO)
        self.add_momentary_button(u'Track_Left', TRACK_LEFT)
        self.add_momentary_button(u'Track_Right', TRACK_RIGHT)

        # Map Track controls
        self.add_matrix(u'Faders', make_slider, 0, [FADERS], MIDI_CC_TYPE)
        self.add_matrix(u'Knobs', make_encoder, 0, [KNOBS], MIDI_CC_TYPE)
        self.add_matrix(u'Mute_Buttons', self.make_toggle_button, 0, [MUTE_BUTTONS], MIDI_CC_TYPE)
        self.add_matrix(u'Solo_Buttons', self.make_toggle_button, 0, [SOLO_BUTTONS], MIDI_CC_TYPE)
        self.add_matrix(u'Rec_Buttons', self.make_toggle_button, 0, [REC_BUTTONS], MIDI_CC_TYPE)
        self.add_matrix(u'Select_Buttons', self.make_toggle_button, 0, [SELECT_BUTTONS], MIDI_CC_TYPE)

    def add_momentary_button(self, name, number):
        assert name not in self.keys()
        self[name] = ButtonElement(True, MIDI_CC_TYPE, 0, number, name=name)

    def make_toggle_button(self, name, channel, number, midi_message_type):
        return ButtonElement(False, midi_message_type, channel, number, name=name)

class NanoKontrolStudio(ControlSurface):

    def __init__(self, *a, **k):
        super(NanoKontrolStudio, self).__init__(*a, **k)
        with self.component_guard():
            midimap = MidiMap()
            
            self._setup_transport_component(midimap)
            self._setup_mixer_component(midimap)

        
    def _setup_transport_component(self, midimap):
        # Build the transport components
        transport = TransportComponent(
            name=u'Transport', 
            is_enabled=False)

        transport.set_play_button(midimap[u'Play'])
        transport.set_stop_button(midimap[u'Stop'])
        transport.set_record_button(midimap[u'Record'])
        transport.set_seek_forward_button(midimap[u'Forward'])
        transport.set_seek_backward_button(midimap[u'Backward'])

        # Test
        midimap['Reset'].set_light(127)

        # Enable component
        transport.set_enabled(True)
    
    def _setup_mixer_component(self, midimap):
        # Build the Mixer with 8 tracks
        mixer_size = 8
        mixer = MixerComponent(
            mixer_size, 
            name=u'Mixer', 
            is_enabled=False)
        
        mixer.set_volume_controls(midimap['Faders'])
        mixer.set_send_controls(midimap['Knobs'])
        mixer.set_mute_buttons(midimap['Mute_Buttons'])
        mixer.set_solo_buttons(midimap['Solo_Buttons'])
        mixer.set_arm_buttons(midimap['Rec_Buttons'])
        mixer.set_track_select_buttons(midimap[u'Select_Buttons'])
        mixer.set_select_buttons(midimap['Track_Right'], midimap['Track_Left'])

        # Enable component
        mixer.set_enabled(True)


