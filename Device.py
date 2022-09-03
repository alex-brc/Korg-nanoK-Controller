class Device:
    class Track:
        Count = 8

        Fader = [2, 3, 4, 5, 6, 8, 9, 12]
        Knob = [13, 14, 15, 16, 17, 18, 19, 20]

        Mute = [21, 22, 23, 24, 25, 26, 27, 28] 
        Solo = [29, 30, 31, 33, 34, 35, 36, 37]
        Rec = [38, 39, 40, 41, 42, 43, 44, 45]
        Select = [46, 47, 48, 49, 50, 51, 52, 53]

        Buttons = [Mute, Solo, Rec, Select]

        Left = 60
        Right = 61
    
    class Transport:
        Cycle = 54

        Rewind = 58
        Forward = 59

        Previous = 62
        Stop = 63
        Play = 80
        Record = 81
    
    class Marker:
        Set = 55
        Left = 56
        Right = 57
    
    class Jogger:
        Sign_Magnitude = 82

        Increment = Clockwise = 83
        Decrement = C_Clockwise = 85

        Continous = 86
        
