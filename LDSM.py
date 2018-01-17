from transitions import Machine


"""LaserDetectorStateMachine
There a five lasers laid out left to right.
There are six states.  

Three states are Left Of the three left lasers.
Three states are Right Of the three right lasers.
The center laser is in both of those counts."""



# Note: Machine.initial( state )


class LDSM():
    def __init__(self):
        """ LO = Left Of
            RO = Right Of

            FL = FarLeft
            L  = Left
            C  = Center
            R  = Right
            FR = FarRight

            So, LO_FL is left of far left."""

        self.states = ['LO_FL', 'LO_L', 'LO_C', 'RO_C', 'RO_R', 'RO_FR']
        # Define with list of lists
        self.transitions = [
            # Left to right transitions.
            ['FarLeftLaser',  'LO_FL', 'LO_L'],
            ['LeftLaser',     'LO_L',  'LO_C'],
            ['CenterLaser',   'LO_C',  'RO_C'],
            ['RightLaser',    'RO_C',  'RO_R'],
            ['FarRightLaser', 'RO_R',  'RO_FR'],
            # Right to left transitions.
            ['FarRightLaser', 'RO_FR', 'RO_R'],
            ['RightLaser',    'RO_R',  'RO_C'],
            ['CenterLaser',   'RO_C',  'LO_C'],
            ['LeftLaser',     'LO_C',  'LO_L'],
            ['FarLeftLaser',  'LO_L',  'LO_FL']
        ]
        self.m = Machine(states=self.states, transitions=self.transitions, initial='LO_C')


    def test(self):

        self.m.to_LO_C()
        self.m.CenterLaser()
        if (self.m.state == 'RO_C'):
            print ( "Good" )

    def test2(self):

        self.initial( self.states[2] )
        self.m.CenterLaser()
        if (self.m.state == 'RO_C'):
            print ( "Good" )


    def initial( self, state ):
        self.m.set_state( state )












if __name__ == "__main__":
    ldsm = LDSM()
    ldsm.test()
    ldsm.test2()
