from Position import Position

class Plant:
    def __init__(self, terrain, id, position=(), regenerate_time=5):
        self.id = id # plant identifier
        self.type = "plant" # book keeping
        self.available = True # is the plant available for consumption by the pray
        self.regenerate_time = regenerate_time # steps taken to regenerate after being consumed
        self.regenerate_countdown = 0 # the plant will regenerate when countdown is 0    
        # plant's location in the terrain
        if len(position)==0: # generate random position
            self.position = Position(0, terrain.width-1, 0, terrain.height-1)
        else:
            self.position = Position(0, terrain.width-1, 0, terrain.height-1, 
                position[0], position[1], random_init=terrain.random_sim)


    def consumed(self): # Q7
        """
            Args:
                self: the plant object
            Returns:
                Nothing
            Behavoir:
                Set plant to unavailable
                Set regenerate_countdown to regenerate_time
        """

        # WRITE YOUR CODE HERE FOR QUESTION 7 (2 lines of code)
        
        # plant no longer available and countdown reset to regen time
        self.available = False
        self.regenerate_countdown = self.regenerate_time
        
    def regenerate(self): # Q8
        """
            Args:
                self: the plant object
            Returns:
                Nothing
            Behavoir:                
                If regenerate_countdown is greater than 0 and plant is not available
                decrease regenerate_countdown by one
                If regenerate_countdown is 0 and plant is not available
                set plant to be available (i.e., regenerated)
            NOTE:
                A plant can reduce regenerate_countdown by one and become available at the 
                same simulation step
        """

        # WRITE YOUR CODE HERE FOR QUESTION 8 (4 lines of code)
        
        # regenrate plant if initially unavailable and regen time completed
        if self.available == False and self.regenerate_countdown > 0:
            self.regenerate_countdown -= 1
            if self.regenerate_countdown == 0:
                self.available = True
                
