from __future__ import absolute_import, print_function, unicode_literals
from _Framework.ButtonMatrixElement import ButtonMatrixElement
from _Framework.ControlSurface import ControlSurface
from _Framework.InputControlElement import MIDI_CC_TYPE
from _Framework.ButtonElement import ButtonElement
from _Framework.Layer import Layer
from _Framework.Resource import SharedResource
from _Framework.TransportComponent import TransportComponent
from _Framework.MixerComponent import MixerComponent
from .component import SessionComponent
from .factory import Factory

# Constants
NUM_TRACKS = 8

# Track controls
FADERS = [2, 3, 4, 5, 6, 8, 9, 12]
KNOBS = [13, 14, 15, 16, 17, 18, 19, 20]
MATRIX_BUTTONS = [
    [21, 22, 23, 24, 25, 26, 27, 28], # Mute
    [29, 30, 31, 33, 34, 35, 36, 37], # Solo
    [38, 39, 40, 41, 42, 43, 44, 45], # Rec
    [46, 47, 48, 49, 50, 51, 52, 53]] # Select

# Jog Wheel
JOG_SIGN_MAGNITUTE = 82
JOG_CLOCKWISE = 83
JOG_INCREMENT = 83
JOG_C_CLOCKWISE = 85
JOG_DECREMENT = 85
JOG_CONTINUOUS = 86

# Transport controls
CYCLE = 54
MARKER_SET = 55
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

class NKS(ControlSurface):

    def __init__(self, *a, **k):
        super(NKS, self).__init__(*a, **k)

        with self.component_guard():
            # Setup Buttons, Faders and Knobs
            self._create_controls()

            # Setup logical components
            self._transport = self._setup_transport_component()
            self._mixer = self._setup_mixer_component()
            self._session = self._setup_session_component()
            self._session.set_mixer(self._mixer)
            self.set_highlighting_session_component(self._session)

            # Activate
            self._transport.set_enabled(True)
            self._mixer.set_enabled(True)
            self._session.set_enabled(True)
    
    def _create_controls(self):
        # Create Shift button
        self._shift_button = Factory.make_button('Shift_Button', CYCLE, resource_type=SharedResource)

        # Create Transport buttons
        self._play_button = Factory.make_button('Play_Button', TRANSPORT_PLAY)
        self._stop_button = Factory.make_button('Stop_Button', TRANSPORT_STOP)
        self._record_button = Factory.make_button('Record_Button', TRANSPORT_RECORD)
        self._fwd_button = Factory.make_button('Forward_Button', TRANSPORT_FORWARD)
        self._rwd_button = Factory.make_button('Rewind_Button', TRANSPORT_REWIND)
        self._set_button = Factory.make_button('Set_Button', MARKER_SET)

        # Create Mixer controls
        self._faders = Factory.make_matrix('Fader', Factory.make_slider, [FADERS])
        self._knobs = Factory.make_matrix('Knob', Factory.make_encoder, [KNOBS])

        # Create the button grid and shift wrapper
        self._mixer_buttons = Factory.make_matrix('Grid_Button', Factory.make_button, MATRIX_BUTTONS)
        self._launch_buttons = Factory.make_shifted_matrix(self._mixer_buttons, self._shift_button)

        # Create Session buttons
        self._track_left = Factory.make_button('Track_Left', TRACK_LEFT)
        self._track_right = Factory.make_button('Track_Right', TRACK_RIGHT)
        self._marker_left = Factory.make_button('Marker_Left', MARKER_LEFT)
        self._marker_right = Factory.make_button('Marker_Right', MARKER_RIGHT)

        # Create Jogger controls
        # 
        
    def _setup_transport_component(self):
        # Build the transport components
        transport = TransportComponent(
            name='Transport', 
            is_enabled=False,
            layer=Layer(
                play_button=self._play_button,
                stop_button=self._stop_button,
                record_button=self._record_button,
                seek_forward_button=self._fwd_button,
                seek_backward_button=self._rwd_button,
                tap_tempo_button=self._set_button
            )
        )
        return transport
    
    def _setup_mixer_component(self):
        # Build the Mixer with 8 tracks
        mixer = MixerComponent(
            num_tracks=8, 
            auto_name=True,
            is_enabled=False,
            layer=Layer(
                volume_controls=ButtonMatrixElement(self._faders),
                send_controls=ButtonMatrixElement(self._knobs),
                mute_buttons=ButtonMatrixElement([self._mixer_buttons[0]]),
                solo_buttons=ButtonMatrixElement([self._mixer_buttons[1]]),
                arm_buttons=ButtonMatrixElement([self._mixer_buttons[2]]),
                track_select_buttons=ButtonMatrixElement([self._mixer_buttons[3]])
            )
        )
        return mixer

    def _setup_session_component(self):
        # Build the 8x4 Session view 
        session = SessionComponent(
            num_tracks=8,
            num_scenes=4,
            auto_name=True,
            is_enabled=False,
            layer=Layer(
                clip_launch_buttons=ButtonMatrixElement(self._launch_buttons), 
                scene_bank_up_button=self._marker_left, 
                scene_bank_down_button=self._marker_right
            )
        )
        session.set_show_highlight(True)
        session.set_offsets(0,0)

        return session

        