from __future__ import absolute_import, print_function, unicode_literals
from functools import partial
import logging
from _Framework.ButtonElement import Color
from _Framework.Task import FadeTask

logger = logging.getLogger(__name__)

class Animation(Color):
    def __init__(self, midi_value, duration, loop, *a, **k):
        super(Animation, self).__init__(midi_value, *a, **k)
        self.duration = duration
        self.loop = loop
        self._state = False
        self._interface = None
    
    def draw(self, interface):
        self._interface = interface
        # Create a task that runs animation() every tick
        interface._animation = FadeTask(self.animation, duration=self.duration, loop=self.loop, init=True)
        # Get task manager for the interface or its parent
        manager = interface._task_group if hasattr(interface, '_task_group') else interface.canonical_parent._task_group
        # Register the task with the manager
        manager.add(interface._animation)

    def animation(self, delta):
        pass


class Pulse(Animation):
    def __init__(self, midi_value=127, duration=0.4, *a, **k):
        super(Pulse, self).__init__(midi_value, duration, loop=True, *a, **k)

    def animation(self, delta):
        if not self._state and delta < self.duration / 2:
            logger.info('Turning button ' + self._interface.name + ' ON')
            self._interface.send_value(Colors.Button.On.midi_value, force=True)
            self._state = True

        elif self._state and delta >= self.duration / 2:         
            logger.info('Turning button ' + self._interface.name + ' OFF')
            self._interface.send_value(Colors.Button.Off.midi_value, force=True)
            self._state = False

class Colors:

    class Button:
        # Standard button colors
        On = Color(127)
        Off = Color(0)

        # Button colors in session mode; standard names
        class Session:
            ClipTriggeredPlay = Pulse(127)      # Trigger to start
            ClipTriggeredRecord = Pulse(127)    # Triggered to record
            ClipStopped = Color(127)            # Clip exists but is stopped
            ClipStarted = Color(127)            # Clip is currently playing 
            ClipRecording = Color(127)          # Clip is currently recording
            RecordButton = Color(0)             # Clip slot is ready to be recorded into (slot with circle))
            # turn_off()                        # Clip does not exist in slot and cannot be recorded into (slot with square)
