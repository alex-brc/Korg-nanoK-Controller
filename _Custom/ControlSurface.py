from __future__ import absolute_import, print_function, unicode_literals
import logging
from _Framework.ControlSurface import ControlSurface as ControlSurfaceBase


class ControlSurface(ControlSurfaceBase):
    def create_elements(self, factory, element, *elements):
        element = [factory(*element)] if not isinstance(element, list) else [self.create_elements(factory, *element)]
        return element if elements is () else element + self.create_elements(factory, *elements)