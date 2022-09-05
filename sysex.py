_SYSEX_START = (240,)
_SYSEX_END= (247,)

class Sysex:
    MANUFACTURER_BYTES = (66, 64, 0, 1, 55)

    class Code:
        ACK = (1, 0, 0, 35)
        NAK = (1, 0, 0, 38)
        UNKNOWN_1_CMD  = (1, 0, 0, 18)
        SCENE_CHANGE_CMD = (2, 0, 0, 20)
        SCENE_CHANGE_EVT = (2, 0, 0, 79)

    @staticmethod
    def get_code(type):
        return vars(Sysex.Code)[type] if type in vars(Sysex.Code) else None

    @staticmethod
    def get_type(code):
        for type, code_for_type in vars(Sysex.Code).items():
            if code_for_type == code:
                return type
        return None

    class Message:
        def __init__(self, code=None, value=None, bytes=()):
            if code is not None and value is not None:
                self.bytes = _SYSEX_START + Sysex.MANUFACTURER_BYTES + code + (value,) + _SYSEX_END
            elif code is not None:
                self.bytes = _SYSEX_START + Sysex.MANUFACTURER_BYTES + code + (value,) + _SYSEX_END
            else:
                assert bytes is not ()
                self.bytes = bytes

        def _get_code(self):
            return self.bytes[6:10]
        code = property(_get_code)

        def _get_value(self):
            return self.bytes[10] if len(self.bytes) == 12 else None
        value = property(_get_value)

        def _get_type(self):
            return Sysex.get_type(self.code)
        type = property(_get_type)

        def to_string(self):
            return '(Type=%s, Code=%s, Value=%s, Raw=%s)' % (self.type, self.code, self.value, self.bytes)

        def __str__(self):
            return self.to_string()

        def __repr__(self):
            return self.to_string()