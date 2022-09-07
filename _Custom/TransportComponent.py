from __future__ import absolute_import, print_function, unicode_literals
import logging
from _Framework.TransportComponent import TransportComponent as TransportComponentBase
from _Framework.ToggleComponent import ToggleComponent
from _Framework.Util import const, negate, nop

class TransportComponent(TransportComponentBase):
    def __init__(self, stop_toggle_view_transform=negate, *a, **k):
        super(TransportComponent, self).__init__(*a, **k)
        self._stop_toggle = self.register_component(ToggleComponent(u'is_playing', self.song(), model_transform=const(False), view_transform=stop_toggle_view_transform))
    
    def _ffwd_value(self, value):
        if value:
            self._ffwd_button.set_light('Pulse')
        else:
            self._ffwd_button.set_light(None)
        super(TransportComponent, self)._ffwd_value(value)
        
    def _rwd_value(self, value):
        if value:
            self._rwd_button.set_light('Pulse')
        else:
            self._rwd_button.set_light(None)
        super(TransportComponent, self)._rwd_value(value)
