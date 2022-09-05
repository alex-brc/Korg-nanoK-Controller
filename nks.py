from __future__ import absolute_import, print_function, unicode_literals
from _Framework.ButtonMatrixElement import ButtonMatrixElement
from _Framework.ControlSurface import ControlSurface
from _Framework.Layer import Layer
from _Framework.ModesComponent import AddLayerMode, ModesComponent
from _Framework.MixerComponent import MixerComponent
from .Component import SelectableModesComponent, SessionComponent, TransportComponent
from .Sysex import Sysex
from .Device import Device
from .Element import ButtonElement, SliderElement, Factory, AnimatedButtonElement, SysexButtonElement

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
        # Creat Scene button
        def __unpack_bytes(value): return value[0]
        self._scene_selector = SysexButtonElement('Scene_Selector', 
            Sysex.Code.SCENE_CHANGE_EVT, Sysex.Code.SCENE_CHANGE_CMD, translate_value=__unpack_bytes)

        # Create Transport buttons
        self._play_button = ButtonElement('Play_Button', Device.Transport.Play)
        self._stop_button = ButtonElement('Stop_Button', Device.Transport.Stop)
        self._record_button = ButtonElement('Record_Button', Device.Transport.Record)
        self._fwd_button = ButtonElement('Forward_Button', Device.Transport.Forward)
        self._rwd_button = ButtonElement('Rewind_Button', Device.Transport.Rewind)

        # Create Mixer controls
        self._faders = Factory.create_matrix(SliderElement, 'Fader', [Device.Track.Fader])
        self._knobs = Factory.create_matrix(SliderElement, 'Knob', [Device.Track.Knob])

        # Create the button grid and shift wrapper
        self._grid_buttons = Factory.create_matrix(AnimatedButtonElement, 'Grid_Button', Device.Track.Buttons)

        # Create Session buttons
        self._session_toggle = ButtonElement('Session_Toggle', Device.Marker.Set)
        self._stop_clips_button = ButtonElement('Stop_Clips_Button', Device.Transport.Previous)

        # Create Jogger controls
        self._jog_wheel = SliderElement('Jog_Wheel', Device.JogWheel.Continous)

        # Other
        self._shift_button = ButtonElement('Shift_Button', Device.Transport.Cycle)
        
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

        session.set_enabled(True)
        self._session = session

    def _setup_component_modes(self):
        # Setup scene modes with selector
        def __redraw_scene(*a): self.update()
        scene_modes = SelectableModesComponent(
            name=u'Scene_Modes', 
            selector=self._scene_selector,
            on_mode_selected=__redraw_scene,
            is_enabled=False)

        # Setup Mixer mode
        scene_modes.add_mode('Mixer_Mode', 
            AddLayerMode(
                self._mixer, 
                layer=Layer(
                    mute_buttons=ButtonMatrixElement([self._grid_buttons[0]]),
                    solo_buttons=ButtonMatrixElement([self._grid_buttons[1]]),
                    arm_buttons=ButtonMatrixElement([self._grid_buttons[2]]),
                    track_select_buttons=ButtonMatrixElement([self._grid_buttons[3]]))),
            selector_value=Device.Scene.Mixer)
        
        # Setup Session mode
        scene_modes.add_mode(u'Session_Mode', 
            AddLayerMode(
                self._session, 
                layer=Layer(
                    clip_launch_buttons=ButtonMatrixElement(self._grid_buttons))),
            selector_value=Device.Scene.Session)
        
        scene_modes.selected_mode = u'Mixer_Mode'
        scene_modes.set_enabled(True)  
    