class CharacterPhysics():
    """
    The mathiest class that handles the physics of moving.

    ---------> x            x grows to right, y grows downwards
    |
    |
    |
    v 
    y
    
    """
    BASEVELOCITY = 5                #These are the constants that are used to calculate character movements.
    MAXFALLVELOCITY = 30
    GRAVITY = 9.81 * 0.01 * 0.3
    BASEJUMP = 15

    def __init__(self, coef = 1) -> None:
        self.xvel = 0
        self.yvel = 0
        self.airtime = 0
        self.speedcoef = coef
        self.falling = True
        self.movingleft = False
        self.movingright = False

    def getPosDelta(self):
        """
        Calculates the change in position based on gravity and airtime and other stuff.
        """
        dx = self.getdx()
        dy = self.getdy()

        return dx, dy

    def getdx(self):
        if self.movingleft and not self.movingright:
            self.xvel = -CharacterPhysics.BASEVELOCITY * self.speedcoef
        elif not self.movingleft and self.movingright:
            self.xvel = CharacterPhysics.BASEVELOCITY * self.speedcoef
        else:
            self.xvel = 0
        dx = self.xvel
        return dx

    def collision(self):
        """
        Stop falling when a collision happens. 
        """
        if self.yvel > 0:       
            self.falling = False
            self.yvel = 0
            self.airtime = 0
        else:
            self.yvel = 0

    def jump(self):
        """
        Gain vertical velocity if on solid ground
        """
        if not self.falling:
            self.falling = True
            self.yvel -= CharacterPhysics.BASEJUMP
        
    def getdy(self):
        '''
        Figure out the change in vertical speed based on falling status
        '''
        if self.falling:
            self.airtime += 1
            if self.yvel < CharacterPhysics.MAXFALLVELOCITY:
                self.yvel += self.airtime * CharacterPhysics.GRAVITY
        
        dy = self.yvel
        return dy