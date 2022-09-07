from __future__ import absolute_import, print_function, unicode_literals
import logging
from _Framework.SessionComponent import SessionComponent as SessionComponentBase
from _Framework.SceneComponent import SceneComponent as SceneComponentBase
from _Framework.ClipSlotComponent import ClipSlotComponent as ClipSlotComponentBase
from _Framework.SubjectSlot import subject_slot
from _Framework.Util import product


class SessionComponent(SessionComponentBase):
    """ Adds support for stopping clips using their corresponding button from the grid """

    class SceneComponent(SceneComponentBase):

        class ClipSlotComponent(ClipSlotComponentBase):
            def __init__(self, *a, **k):
                super(SessionComponent.SceneComponent.ClipSlotComponent, self).__init__(*a, **k)
                self._stopping = False
                self._triggered_to_stop_value = 127

            def set_stop_button(self, button):
                self._stop_button_value.subject = button
                self.update()

            def set_triggered_to_stop_value(self, value):
                self._triggered_to_stop_value = value

            def update(self):
                super(SessionComponent.SceneComponent.ClipSlotComponent, self).update()
                button = self._stop_button_value.subject
                if self._allow_updates:
                    if self.is_enabled() and button != None:
                        value_to_send = self._feedback_value()
                        if self._stopping:
                            value_to_send = self._triggered_to_stop_value
                            self._stopping = False
                        if value_to_send in (None, self._stopped_value, -1):
                            button.turn_off()
                        elif value_to_send in range(0, 128):
                            button.send_value(value_to_send)
                        else:
                            button.set_light(value_to_send)
                else:
                    self._update_requests += 1
            
            def _do_stop_clip(self, value):
                button = self._stop_button_value.subject
                clip = self._clip_slot.clip if self.has_clip() else self._clip_slot
                if (not button.is_momentary() and value) or (button.is_momentary() and not value):
                    clip.stop()
                self._stopping = True
                self.update()

            @subject_slot(u'value')
            def _stop_button_value(self, value):
                self._do_stop_clip(value)

        clip_slot_component_type = ClipSlotComponent

    scene_component_type = SceneComponent
    
    def set_clip_stop_buttons(self, buttons):
        assert not buttons or buttons.width() == self._num_tracks and buttons.height() == self._num_scenes
        if buttons:
            for button, (x, y) in buttons.iterbuttons():
                scene = self.scene(y)
                slot = scene.clip_slot(x)
                slot.set_stop_button(button)
                slot.set_triggered_to_stop_value(self._stop_clip_triggered_value)

        else:
            for x, y in product(range(self._num_tracks), range(self._num_scenes)):
                scene = self.scene(y)
                slot = scene.clip_slot(x)
                slot.set_stop_button(None)
    
    def _can_bank_down(self):
        return len(self.song().scenes) - self._num_scenes + 1 > self._get_minimal_scene_offset() + 1

    def _can_bank_right(self):
        return len(self.tracks_to_use()) - self._num_tracks + 1 > self._get_minimal_track_offset() + 1
