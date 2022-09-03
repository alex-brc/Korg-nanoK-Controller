class SysexMessage:

        ACK = (1, 0, 0, 35)

        UNKNOWN_1_CMD = (1, 0, 0, 18)

        SCENE_CHANGE_CMD = (2, 0, 0, 20)        
        SCENE_CHANGE_EVT = (2, 0, 0, 79)

        def __init__(self, code=None, value=None, bytes=()):
            if code is not None and value is not None:
                self.code, self.value = (code, value)
                self.bytes = (240, 66, 64, 0, 1, 55) + code + (value, 247)
            else:
                self.code, self.value = (bytes[6:10], bytes[10])
                self.bytes = bytes
                
        