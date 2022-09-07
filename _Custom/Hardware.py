class Hardware:

    class Scene:
        Count = 4

        Mixer = 0
        Session = 1
        Device = 2

    class Track:
        Count = 8
        
        Fader = [('Fader_0', 2), ('Fader_1', 3), ('Fader_2', 4), ('Fader_3', 5), ('Fader_4', 6), ('Fader_5', 8), ('Fader_6', 9), ('Fader_7', 12)]
        Knob = [('Knob_0', 13), ('Knob_1', 14), ('Knob_2', 15), ('Knob_3', 16), ('Knob_4', 17), ('Knob_5', 18), ('Knob_6', 19), ('Knob_7', 20)]

        Mute = [('Mute_Button_0', 21), ('Mute_Button_1', 22), ('Mute_Button_2', 23), ('Mute_Button_3', 24), ('Mute_Button_4', 25), ('Mute_Button_5', 26), ('Mute_Button_6', 27), ('Mute_Button_7', 28)]
        Solo = [('Solo_Button_0', 29), ('Solo_Button_1', 30), ('Solo_Button_2', 31), ('Solo_Button_3', 33), ('Solo_Button_4', 34), ('Solo_Button_5', 35), ('Solo_Button_6', 36), ('Solo_Button_7', 37)]
        Record = [('Rec_Button_0', 38), ('Rec_Button_1', 39), ('Rec_Button_2', 40), ('Rec_Button_3', 41), ('Rec_Button_4', 42), ('Rec_Button_5', 43), ('Rec_Button_6', 44), ('Rec_Button_7', 45)]
        Select = [('Select_Button_0', 46), ('Select_Button_1', 47), ('Select_Button_2', 48), ('Select_Button_3', 49), ('Select_Button_4', 50), ('Select_Button_5', 51), ('Select_Button_6', 52), ('Select_Button_7', 53)]

        Left = 'Track_Left_Button', 60
        Right = 'Track_Right_Button', 61
    
    class Transport:
        Cycle = 'Cycle_Button', 54

        Rewind = 'Rewind_Button', 58
        Forward = 'Forward_Button', 59

        Previous = 'Previous_Button', 62
        Stop = 'Stop_Button', 63
        Play = 'Play_Button', 80
        Record = 'Record_Button', 81
    
    class Marker:
        Set = 'Set_Button', 55
        Left = 'Marker_Left_Button', 56
        Right = 'Marker_Right_Button', 57
    
    class JogWheel:
        Sign_Magnitude = 'Jog_Sign_Magnitude', 82

        Increment = Clockwise = 'Jog_Increment_Input', 83
        Decrement = C_Clockwise = 'Jog_Decrement_Input', 85

        Continous = 'Jog_Continuous_Input', 86
        
