from __future__ import absolute_import, print_function, unicode_literals
from _Framework.ButtonMatrixElement import ButtonMatrixElement
from _Framework.ControlSurface import ControlSurface
from _Framework.InputControlElement import MIDI_CC_TYPE
from _Framework.ButtonElement import ButtonElement
from _Framework.Layer import Layer
from _Framework.ModesComponent import AddLayerMode, ModesComponent
from _Framework.Resource import SharedResource
from _Framework.TransportComponent import TransportComponent
from _Framework.MixerComponent import MixerComponent
from _Framework.Util import nop
from .component import SessionComponent
from .factory import Factory
from .sysex import SysexMessage

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
            self._setup_transport_component()
            self._setup_mixer_component()
            self._setup_session_component()
            self._session.set_mixer(self._mixer)

            # Create modes for the button grid
            self._setup_component_modes()
    
    def _create_controls(self):
        # Create Transport buttons
        self._play_button = Factory.make_button('Play_Button', TRANSPORT_PLAY)
        self._stop_button = Factory.make_button('Stop_Button', TRANSPORT_STOP)
        self._record_button = Factory.make_button('Record_Button', TRANSPORT_RECORD)
        self._fwd_button = Factory.make_button('Forward_Button', TRANSPORT_FORWARD)
        self._rwd_button = Factory.make_button('Rewind_Button', TRANSPORT_REWIND)
        self._mode_toggle = Factory.make_toggle('Mode_Toggle', MARKER_SET)

        # Create Mixer controls
        self._faders = Factory.make_matrix('Fader', Factory.make_slider, [FADERS])
        self._knobs = Factory.make_matrix('Knob', Factory.make_encoder, [KNOBS])

        # Create the button grid and shift wrapper
        self._grid_buttons = Factory.make_matrix('Grid_Button', Factory.make_button, MATRIX_BUTTONS)

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
                seek_backward_button=self._rwd_button
            )
        )
        transport.set_enabled(True)
        self._transport = transport
    
    def _setup_mixer_component(self):
        # Build the Mixer with 8 tracks
        mixer = MixerComponent(
            num_tracks=8, 
            auto_name=True,
            is_enabled=False,
            layer=Layer(
                # mute_buttons=ButtonMatrixElement([self._mixer_buttons[0]]),
                # solo_buttons=ButtonMatrixElement([self._mixer_buttons[1]]),
                # arm_buttons=ButtonMatrixElement([self._mixer_buttons[2]]),
                # track_select_buttons=ButtonMatrixElement([self._mixer_buttons[3]]),
                volume_controls=ButtonMatrixElement(self._faders),
                send_controls=ButtonMatrixElement(self._knobs)
            )
        )
        mixer.set_enabled(True)
        self._mixer = mixer

    def _setup_session_component(self):
        # Build the 8x4 Session view 
        session = SessionComponent(
            num_tracks=8,
            num_scenes=4,
            auto_name=True,
            is_enabled=False,
            layer=Layer(
                # clip_launch_buttons=ButtonMatrixElement(self._launch_buttons), 
                scene_bank_up_button=self._marker_left, 
                scene_bank_down_button=self._marker_right
            )
        )
        session.set_show_highlight(True)
        session.set_offsets(0,0)
        self.set_highlighting_session_component(session)

        session.set_enabled(True)
        self._session = session

    def _setup_component_modes(self):
        # Setup modes with selector
        grid_modes = ModesComponent(name=u'Grid Modes', is_enabled=False)
        grid_modes.set_toggle_button(self._mode_toggle)

        # Setup Mixer mode
        grid_modes.add_mode(u'mixer', 
            AddLayerMode(
                self._mixer, 
                layer=Layer(
                    mute_buttons=ButtonMatrixElement([self._grid_buttons[0]]),
                    solo_buttons=ButtonMatrixElement([self._grid_buttons[1]]),
                    arm_buttons=ButtonMatrixElement([self._grid_buttons[2]]),
                    track_select_buttons=ButtonMatrixElement([self._grid_buttons[3]]))),
            toggle_value=False)
        
        # Setup Session mode
        grid_modes.add_mode(u'session', 
            AddLayerMode(
                self._session, 
                layer=Layer(
                    clip_launch_buttons=ButtonMatrixElement(self._grid_buttons))),
            toggle_value=True)
        
        grid_modes.selected_mode = u'mixer'
        grid_modes.set_enabled(True)  
    
    def handle_sysex(self, midi_bytes):
        sysex = SysexMessage(bytes=midi_bytes)

        # LEDs go dark after Scene button is pressed, redraw 
        if sysex.code == SysexMessage.SCENE_CHANGE_EVT:
            # If Scene is changed to something outside usable range, go back to first scene
            if sysex.value > 1:
                self.log_message('Scene change attempted; resetting scene to 0; args: ' + str(midi_bytes))
                # Mystery command also supposed to be here? Not sure why
                # self._send_midi(SysexMessage(SysexMessage.UNKNOWN_1_CMD, 0).bytes)
                # Set Scene to 0
                self._send_midi(SysexMessage(SysexMessage.SCENE_CHANGE_CMD, 0).bytes)
            # Else, Scene is accepted and a refresh is needed
            else:
                self.log_message('Acceptable scene change; args: ' + str(midi_bytes))
                self.update()
        # After setting the Scene on device, an ACK is returned, a refresh is also needed
        elif sysex.code == SysexMessage.ACK:
            self.log_message('Received ACK; args: ' + str(midi_bytes))
            self.update()
        else:
            self.show_message('Received SYSEX with args: ' + str(midi_bytes))
        
        
    def handle_nonsysex(self, midi_bytes):
        # self.show_message('Received MIDI with args: ' + str(midi_bytes))

        super(NKS, self).handle_nonsysex(midi_bytes)

        