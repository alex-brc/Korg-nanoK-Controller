from __future__ import absolute_import, print_function, unicode_literals
from _Framework.SessionComponent import SessionComponent as SessionComponentBase

class SessionComponent(SessionComponentBase):

    def set_offsets_from_scene(self, scene_number):
        self.set_offsets(self.track_offset(), scene_number)

    def _can_bank_down(self):
        return len(self.song().scenes) - self._num_scenes + 1 > self._get_minimal_scene_offset() + 1

    def _can_bank_right(self):
        return len(self.tracks_to_use()) - self._num_tracks + 1 > self._get_minimal_track_offset() + 1