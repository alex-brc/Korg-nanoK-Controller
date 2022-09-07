from __future__ import absolute_import, print_function, unicode_literals
import logging
from _Framework.ModesComponent import ModesComponent as ModesComponentBase
from _Framework.CompoundComponent import CompoundComponent
from _Framework.SubjectSlot import subject_slot


class SceneSelectorComponent(CompoundComponent):
    __subject_events__ = (u'selected_scene',)

    def __init__(self, selector, *a, **k):
        super(SceneSelectorComponent, self).__init__(*a, **k)
        assert selector is not None
        self._num_scenes=0
        self._selected_scene = None
        self._scene_map = {}
        self._selector = selector
        selector.send_value(0)
        self._on_selector_value_changed.subject = selector

    def add_scene(self, index, modes):
        assert isinstance(modes, ModesComponentBase)
        assert index is not None and index not in self._scene_map
        self._num_scenes += 1
        self._scene_map[index] = modes
        
    def cycle_scenes(self, steps=1):
        self._set_selected_scene((self.selected_scene + steps) % self._num_scenes, update_hardware=True)
        
    def _set_selected_scene(self, value, update_hardware=False):
        if self._num_scenes is not None and value >= self._num_scenes:
            value = 0
            update_hardware = True

        if self._selected_scene is not None:
            self._scene_map[self._selected_scene].set_enabled(False)
        
        if value in self._scene_map:
            self._scene_map[value].set_enabled(True)
            self._selected_scene = value

        self.notify_selected_scene(value)
        if update_hardware: 
            self.update_hardware(value)

    def _get_selected_scene(self):
        return self._selected_scene
    
    selected_scene = property(_get_selected_scene, _set_selected_scene)

    def update_hardware(self, value):
        self._selector.send_value(value)
    
    @subject_slot(u'value')
    def _on_selector_value_changed(self, value):
        self._set_selected_scene(value)
