from __future__ import absolute_import, print_function, unicode_literals
from _Framework.ButtonMatrixElement import ButtonMatrixElement
from _Framework.ControlSurface import ControlSurface
from _Framework.Layer import Layer
from _Framework.ModesComponent import AddLayerMode, ModesComponent
from _Framework.TransportComponent import TransportComponent
from _Framework.MixerComponent import MixerComponent
from .Component import SessionComponent
from .Sysex import SysexMessage
from .Element import ButtonElement, SliderElement, Factory, StopButtonElement, SessionButtonElement
from .Device import Device

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
        # Creat shift button
        self._shift_button = ButtonElement('Shift_Button', Device.Transport.Cycle)

        # Create Transport buttons
        self._play_button = ButtonElement('Play_Button', Device.Transport.Play)
        self._stop_button = StopButtonElement('Stop_Button', Device.Transport.Stop)
        self._record_button = ButtonElement('Record_Button', Device.Transport.Record)
        self._fwd_button = ButtonElement('Forward_Button', Device.Transport.Forward)
        self._rwd_button = ButtonElement('Rewind_Button', Device.Transport.Rewind)

        # Create Mixer controls
        self._faders = Factory.create_matrix(SliderElement, 'Fader', [Device.Track.Fader])
        self._knobs = Factory.create_matrix(SliderElement, 'Knob', [Device.Track.Knob])

        # Create the button grid and shift wrapper
        self._grid_buttons = Factory.create_matrix(
            SessionButtonElement, 
            'Grid_Button', 
            Device.Track.Buttons)

        # Create Session buttons
        self._session_toggle = ButtonElement('Session_Toggle', Device.Marker.Set)
        self._stop_clips_button = ButtonElement('Stop_Clips_Button', Device.Transport.Previous)

        # Create Jogger controls
        # 

        # Other
        self._track_left = ButtonElement('Track_Left', Device.Track.Left)
        self._track_right = ButtonElement('Track_Right', Device.Track.Right)
        self._marker_left = ButtonElement('Marker_Left', Device.Marker.Left)
        self._marker_right = ButtonElement('Marker_Right', Device.Marker.Right)
        
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
        # Stop button is reactive to the Transport state
        self._stop_button.set_transport(transport)

        transport.set_enabled(True)
        self._transport = transport
    
    def _setup_mixer_component(self):
        # Build the Mixer with 8 tracks
        mixer = MixerComponent(
            num_tracks=8, 
            auto_name=True,
            is_enabled=False,
            layer=Layer(
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
            enable_skinning=True,
            is_enabled=False,
            layer=Layer(
                stop_all_clips_button=self._stop_clips_button
            )
            # Scene button on controller moves session bank
        )
        session.set_show_highlight(True)
        self.set_highlighting_session_component(session)

        ## self._session_toggle.add_value_listener(_reset_grid_colors, identify_sender=False)

        session.set_enabled(True)
        self._session = session

    def _setup_component_modes(self):
        # Setup modes with selector
        grid_modes = ModesComponent(name=u'Grid_Modes', is_enabled=False)
        grid_modes.set_toggle_button(self._session_toggle)

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

        # Received when Scene button is pressed on controller
        if sysex.code == SysexMessage.SCENE_CHANGE_EVT:
            self._session.set_offsets_from_scene(sysex.value)
            # LEDs go dark after Scene button is pressed, redraw 
            self.update()
        elif sysex.code == SysexMessage.ACK:
            self.log_message('Received ACK; args: ' + str(sysex.bytes))
        elif sysex.code == SysexMessage.NAK:
            self.show_message('Received NAK; args: ' + str(sysex.bytes))
        else:
            self.show_message('Received SYSEX with args: ' + str(midi_bytes))
        