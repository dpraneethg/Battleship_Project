""" ship.py 
Defines the Ship class used by the Battleship game. """

from rich.console import Console
from rich.panel import Panel
from rich.align import Align
console = Console()

class Ship:
    def __init__(self, name, size):

        """Initializing Ship."""

        self.name = name
        self.size = size
        self.coords = []
        self.hits = []

    def place(self, row, column, orientation):

        """Stores the Coordinates of the Ship. Not checking the validity of
           inputs received as that is done by place_ship() in board.py"""

        self.coords = []
        orientation = orientation.upper()
        self.orientation = orientation
        if (orientation == "H"):
            for i in range(self.size):
                self.coords.append((row, column + i))
        else:
            for i in range(self.size):
                self.coords.append((row + i, column))
    
    def is_at(self, x, y):

        """Checks if the ship is present at the given coordinates."""

        if ((x, y) in self.coords): return True
        return False
    
    def register_hit(self, x, y):

        """If the shot is a hit, it verifies and stores the hit location, else returns False."""

        if ((x, y) in self.coords and (x, y) not in self.hits):
            self.hits.append((x, y))
            return True
        return False
    
    def is_sunk(self):

        """Checks if the ship is sunk or not."""

        if (len(self.coords) == len(self.hits)): return True
        return False
    
    def to_dict(self):
        """Saves the ship info in a dictionary"""
        return {
            "name" : self.name,
            "size" : self.size,
            "coords" : self.coords,
            "hits" : self.hits
        }
    
    @classmethod
    def from_dict(cls, data):
        """Creates a ship object from data saved"""
        ship = cls(data["name"], data["size"])
        ship.coords = [tuple(x) for x in data["coords"]]
        ship.hits = [tuple(x) for x in data["hits"]]
        return ship

def notify(message, type = "info"):
    styles = {
        "info": "bold cyan",
        "success": "bold green",
        "warning": "bold yellow",
        "error": "bold red"
    }
    style = styles.get(type)
    panel = Panel(message, style = style, expand = False)
    centered_panel = Align.center(panel)
    console.print(centered_panel)