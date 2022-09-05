from __future__ import absolute_import, print_function, unicode_literals
import logging
from _Framework.ModesComponent import ModesComponent as ModesComponentBase
from _Framework.SessionComponent import SessionComponent as SessionComponentBase
from _Framework.ToggleComponent import ToggleComponent
from _Framework.TransportComponent import TransportComponent as TransportComponentBase
from _Framework.SubjectSlot import subject_slot
from _Framework.Util import const, negate, nop
logger = logging.getLogger(__name__)

class SelectableModesComponent(ModesComponentBase):
    """ Supports the use of a Selector, which must support a value listener.
        Attaches a value listener to the given Selector which sets the selected
        mode based on the value. """
    
    def __init__(self, selector=None, on_mode_selected=nop, *a, **k):
        super(SelectableModesComponent, self).__init__(*a, **k)
        self._selector_map = {}
        self._on_mode_selected = on_mode_selected
        self.set_selector(selector)
    
    def add_mode(self, name, mode_or_component, selector_value=None):
        super(SelectableModesComponent, self).add_mode(name, mode_or_component)
        if selector_value is not None:
            assert selector_value not in self._selector_map, u'Duplicate selector values for modes component'
            self._selector_map[selector_value] = name
    
    def select_mode(self, value, selector=None):
        target_mode = self._selector_map[value] if value in self._selector_map else None
        logging.info('Selecting mode #%s with name %s' % (value, target_mode))
        self.selected_mode = target_mode
        self._on_mode_selected(target_mode)
    
    def set_selector(self, selector):
        if selector is not None:
            self._selector = selector
            self._on_selector_value_changed.subject = selector
            
    @subject_slot(u'value')
    def _on_selector_value_changed(self, value):
        self.select_mode(value)


class SessionComponent(SessionComponentBase):

    def set_offsets_from_scene(self, scene_number):
        self.set_offsets(self.track_offset(), scene_number)

    def _can_bank_down(self):
        return len(self.song().scenes) - self._num_scenes + 1 > self._get_minimal_scene_offset() + 1

    def _can_bank_right(self):
        return len(self.tracks_to_use()) - self._num_tracks + 1 > self._get_minimal_track_offset() + 1

class TransportComponent(TransportComponentBase):
    def __init__(self, stop_toggle_view_transform=negate, *a, **k):
        super(TransportComponent, self).__init__(*a, **k)
        self._stop_toggle = self.register_component(ToggleComponent(u'is_playing', self.song(), model_transform=const(False), view_transform=stop_toggle_view_transform))