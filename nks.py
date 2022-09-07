from __future__ import absolute_import, print_function, unicode_literals
from _Framework.ButtonMatrixElement import ButtonMatrixElement
from _Framework.Layer import Layer
from _Framework.ModesComponent import AddLayerMode, ModesComponent
from ._Custom.Hardware import Hardware
from ._Custom.Sysex import Sysex
from ._Custom.ControlSurface import ControlSurface
from ._Custom.SceneSelectorComponent import SceneSelectorComponent
from ._Custom.TransportComponent import TransportComponent
from ._Custom.MixerComponent import MixerComponent
from ._Custom.SessionComponent import SessionComponent
from ._Custom.ButtonElement import ButtonElement, AnimatedButtonElement, SysexButtonElement
from ._Custom.SliderElement import SliderElement

class NKS(ControlSurface):

    def __init__(self, *a, **k):
        super(NKS, self).__init__(*a, **k)

        with self.component_guard():
            # Setup Buttons, Faders and Knobs
            self._create_controls()

            # Setup logical components
            self._setup_transport_component()
            mixer_modes = self._setup_mixer_component()
            session_modes = self._setup_session_component()

            # Create modes for the button grid
            self._setup_scenes(mixer_modes, session_modes)
            
        
    def _create_controls(self):
        # Creat Scene button
        def __unpack_bytes(value): return value[0]
        self._scene_button = SysexButtonElement('Scene_Selector', Sysex.Code.SCENE_CHANGE_EVT, Sysex.Code.SCENE_CHANGE_CMD, translate_value=__unpack_bytes)

        # Create Transport buttons
        self._play_button, self._stop_button, self._record_button, self._previous_button, self._track_left, self._track_right, self._cycle_button, self._marker_left, self._marker_right, self._marker_set = \
            self.create_elements(ButtonElement, Hardware.Transport.Play, Hardware.Transport.Stop, Hardware.Transport.Record, Hardware.Transport.Previous, Hardware.Track.Left, Hardware.Track.Right, Hardware.Transport.Cycle, Hardware.Marker.Left, Hardware.Marker.Right, Hardware.Marker.Set)
        self._fwd_button, self._rwd_button = self.create_elements(AnimatedButtonElement, Hardware.Transport.Forward, Hardware.Transport.Rewind)
        # Create Mixer controls
        self._faders, self._knobs = self.create_elements(SliderElement, Hardware.Track.Fader, Hardware.Track.Knob)

        # Create the button grid
        self._mute_buttons, self._solo_buttons, self._rec_buttons, self._sel_buttons = \
            self.create_elements(AnimatedButtonElement, Hardware.Track.Mute, Hardware.Track.Solo, Hardware.Track.Record, Hardware.Track.Select)
        self._button_grid = [self._mute_buttons, self._solo_buttons, self._rec_buttons, self._sel_buttons]

        # Create Jogger controls
        self._jog_wheel = self.create_elements(SliderElement, Hardware.JogWheel.Continous)

        
    def _setup_transport_component(self):
        # Build the transport components
        transport = TransportComponent(
            name='Transport', 
            is_enabled=False,
            layer=Layer(
                play_button=self._play_button,
                stop_button=self._stop_button,
                record_button=self._record_button,
                seek_backward_button=self._rwd_button,
                seek_forward_button=self._fwd_button,))

        transport.set_enabled(True)
        self._transport = transport
    
    def _setup_mixer_component(self):
        # Build the Mixer with 8 tracks
        mixer = MixerComponent(
            num_tracks=Hardware.Track.Count, 
            auto_name=True,
            is_enabled=False,
            layer=Layer(
                volume_controls=ButtonMatrixElement([self._faders]),
                send_controls=ButtonMatrixElement([self._knobs])))

        mixer.set_select_buttons(self._track_right, self._track_left)
        mixer.set_enabled(True)

        # Setup Mixer modes
        mixer_modes = ModesComponent(
            name='Mixer_Modes',
            is_enabled=False)
        mixer_modes.add_mode('Mixer', AddLayerMode(mixer, layer=Layer(
                mute_buttons=ButtonMatrixElement([self._mute_buttons]),
                solo_buttons=ButtonMatrixElement([self._solo_buttons]),
                arm_buttons=ButtonMatrixElement([self._rec_buttons]),
                track_select_buttons=ButtonMatrixElement([self._sel_buttons]))),
            toggle_value=False)
        mixer_modes.add_mode('Mixer_Alt', AddLayerMode(mixer, layer=Layer()),
            toggle_value=True)
        mixer_modes.set_toggle_button(self._marker_set)
        mixer_modes.selected_mode = 'Mixer'

        self._mixer = mixer
        return mixer_modes

    def _setup_session_component(self):
        # Build the 8x4 Session view 
        session = SessionComponent(
            num_tracks=8,
            num_scenes=4,
            auto_name=True,
            enable_skinning=True,
            is_enabled=False,
            layer=Layer(
                stop_all_clips_button=self._previous_button))

        session.set_show_highlight(True)
        session.set_mixer(self._mixer)
        session.set_enabled(True)
        self.set_highlighting_session_component(session)

        # Create modes
        session_modes = ModesComponent(
            name='Session_Modes',
            is_enabled=False)
        session_modes.add_mode(u'Session', AddLayerMode(session, layer=Layer(
                scene_bank_up_button=self._marker_left,
                scene_bank_down_button=self._marker_right,
                clip_launch_buttons=ButtonMatrixElement(self._button_grid))),
            toggle_value=False)
        session_modes.add_mode(u'Session_Alt', AddLayerMode(session, layer=Layer(
                scene_bank_up_button=self._marker_left,
                scene_bank_down_button=self._marker_right,
                clip_stop_buttons=ButtonMatrixElement(self._button_grid))),
            toggle_value=True)
        session_modes.set_toggle_button(self._marker_set)
        session_modes.selected_mode = 'Session'

        self._session = session
        return session_modes
    
    def _setup_device_component():
        pass

    def _setup_scenes(self, mixer_modes, session_modes):
        # Setup scene modes with selector
        def _redraw(*a): self.update()
        scene_selector = SceneSelectorComponent(
            selector=self._scene_button,
            is_enabled=False)
        scene_selector.add_selected_scene_listener(_redraw)

        # Cycle button is scuffed, stops other button MIDIs from being sent from device. Use as alternate Scene button
        def _cycle_scenes(value, button): 
            if value: 
                scene_selector.cycle_scenes(1)
                button.set_light('Enabled')
            else:
                button.turn_off()

        self._cycle_button.add_value_listener(_cycle_scenes, True)

        scene_selector.add_scene(Hardware.Scene.Mixer, mixer_modes)
        scene_selector.add_scene(Hardware.Scene.Session, session_modes)
        scene_selector.selected_scene = Hardware.Scene.Mixer

        scene_selector.set_enabled(True)  
        self._scene_selector = scene_selector
    
    def update(self):
        super(NKS, self).update()
        # Track left/right selectors do no correctly update by themselves
        self._mixer.on_selected_track_changed()

    
    def handle_sysex(self, midi_bytes):
        sysex = Sysex.Message(bytes=midi_bytes)
        if sysex.code not in (Sysex.Code.ACK, Sysex.Code.NAK):
            super(NKS, self).handle_sysex(midi_bytes)