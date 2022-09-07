from __future__ import absolute_import, print_function, unicode_literals
import logging
from _Framework.MixerComponent import MixerComponent as MixerComponentBase

class MixerComponent(MixerComponentBase):

    def on_selected_track_changed(self):
        devices = self.song().view.selected_track.devices
        self.canonical_parent.show_message('Device: %s' % str(len(devices)))
        super(MixerComponent, self).on_selected_track_changed()
