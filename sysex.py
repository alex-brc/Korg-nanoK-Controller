class SysexMessage:
        _SYSEX_HEADER = (240, 66, 64, 0, 1, 55)

        ACK = (1, 0, 0, 35)
        NAK = (1, 0, 0, 38)

        UNKNOWN_1_CMD = (1, 0, 0, 18)

        SCENE_CHANGE_CMD = (2, 0, 0, 20)        
        SCENE_CHANGE_EVT = (2, 0, 0, 79)

        def __init__(self, code=None, value=None, bytes=()):
            if code is not None and value is not None:
                self.code, self.value = (code, value)
                self.bytes =  + code + (value, 247)
            else:
                if len(bytes) == 11:
                    self.code, self.value = (bytes[6:10], None)
                else:
                    self.code, self.value = (bytes[6:10], bytes[10])

                self.bytes = bytes
                
        