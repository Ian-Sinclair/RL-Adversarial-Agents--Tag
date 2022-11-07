"""
        Stores object classes for default objects and empty space.
"""


class object :
    def __init__( self, 
                symbol : set = set(' '),
                name : str = None ,
                color : str = 'black' ,
                gif = None , 
                 ) :
        self.symbol = symbol
        self.color = color 
        self.name = name
        self.gif = gif
    
    def getInfo(self) :
        return {'Name' : self.name,
                'Symbol' : self.symbol ,
                'Color' : self.color ,
                'gif_location' : self.gif}
        

class wall( object ) :
    def __init__( self, 
                symbol : set = set('W'),
                name : str = 'Wall' ,
                color : str = 'black' ,
                gif = None , 
                threat : int = 10
                 ) :
        object.__init__(self, 
                symbol = symbol,
                name = name ,
                color = color ,
                gif = gif )
        self.threat = threat # threat could be damage done if touched

class empty( object ) :
    def __init__(self, 
                symbol : str = set(' '),
                name : str = 'Empty Space' ,
                color : str = None ,
                gif = None , 
                threat : int = 0
                ) :
        object.__init__(self, 
                symbol = symbol,
                name = name ,
                color = color ,
                gif = gif )
        self.threat = threat # threat could be damage done if touched
        

