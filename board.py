import random
from ship import Ship
from rich.console import Console
from rich.table import Table
from rich.align import Align
console = Console()

dict1={
    'A':1,'B':2,'C':3,'D':4,'E':5,'F':6,'G':7,'H':8,'I':9,'J':10
}

#to convert coodinates from alpha numerical to purely numerical coordinates
def alpha_to_num(coordinate):
    if not coordinate:
        return None
    letter=coordinate[0].upper()
    number=coordinate[1:]
    if letter not in dict1 or not number.isdigit():
        return None
    number=int(number)
    letter=dict1[letter]
    if 1<=number<=10:
        return letter,number
    return None

#to convert purely numerical coordinates to Alpha numerical coordinates
def num_to_alpha(row,column):
    return f"{chr(64+row)}{column}"

#the board class
class Board:
    #the constructor(defines the board grid)
    def __init__(self):
        self.grid = [["~"for i in range(10)]for j in range(10)]
        self.ships={}
        self.misses = []

    #function to check whether we can place the ship in the particular orientation and position or not
    def can_place(self,orientation,row,column,size):
        if orientation=="H":
            if column+size>11:
                return False
            for i in range(size):
                if(self.grid[row-1][column+i-1]!="~"):
                    return False
            return True
        if orientation=='V':
            if row+size>11:
                return False
            for i in range(size):
                if self.grid[row+i-1][column-1]!="~":
                    return False
            return True
        return False
    
    #function which helps us place the ships on the board and helps us update the grid
    def place_ship(self,ship : Ship,orientation,row,column):
        if not self.can_place(orientation,row,column,ship.size):
            return False
        else:
            points=[]
            if orientation=="H":
                points=[(row,column+i) for i in range(ship.size)]
            else:
                points=[(row+i,column) for i in range(ship.size)]
            for pt in points:
                self.grid[pt[0]-1][pt[1]-1]="S"
            ship.place(row, column, orientation)
            self.ships[ship.name] = ship
            return True

    #function to place the ships randomly in case the player chooses to do so    
    def place_random(self,ship_specs):
        for name,size in ship_specs:
            placed=False
            tries=0
            while not placed and tries<2000:
                tries+=1
                orient=random.choice(["H","V"])
                row=random.randrange(1,11)
                column=random.randrange(1,11)
                s=Ship(name=name,size=size)
                if self.place_ship(s, orient, row, column):
                    placed = True
                    self.ships[s.name]=s

    #checks if the particular cell can be fired at and updates the cell according to hit or miss
    def receive_fire(self,row,column):
        tile = self.grid[row-1][column-1]
        if tile == "X" or tile == "O":
            return (None, None) 
            
        if tile == "S":
            for ship in self.ships.values():
                if ship.register_hit(row, column):
                    self.grid[row-1][column-1] = "X"
                    if ship.is_sunk():
                        return (True, ship.name)
                    return (True, None)
            self.grid[row-1][column-1] = "X"
            return (True, None)
        else:
            self.grid[row-1][column-1] = "O"
            self.misses.append((row, column))
            return (False, None)
    
    #returns True if all ships on board are sunk else returns False
    def all_sunk(self):
        for ship in self.ships.values():
            if not ship.is_sunk():
                return False
        return True
    
    #function to print the board in the console and display the current status of the board
    def display(self, player, s = False):
        grid = Table(title = player, title_style = "bold")
        grid.add_column(" ", width = 3)
        for col in range(1, 11):
            grid.add_column(str(col), justify="center", style = "cyan", width = 3)
        for i in range(10):
            row_label = chr(65+i)
            row = [row_label]
            for j in range(10):
                cell = self.grid[i][j]
                if (cell == "X"):
                    row.append("[bold red]X[/bold red]")
                elif (cell == "O"):
                    row.append("[bold yellow]O[/bold yellow]")
                elif (cell == "S" and s):
                    row.append("[bold green]S[/bold green]")
                else:
                    row.append("[bold blue]~[/bold blue]")
            grid.add_row(*row, end_section = True)
        centered_grid = Align.center(grid)
        console.print(centered_grid)

    def to_dict(self):
        """Saves board data to a dictionary"""
        misses = []
        for i in range(10):
            for j in range(10):
                if self.grid[i][j] == "O":
                    misses.append((i+1, j+1))
        return {
            "ships": [ship.to_dict() for ship in self.ships.values()],
            "misses": misses
        }
    
    @classmethod
    def from_dict(cls, data):
        """Reconstructs board from saved data"""
        board = cls()
        ships_list = data.get("ships", [])
        for ship_data in ships_list:
            ship = Ship.from_dict(ship_data)
            board.ships[ship.name] = ship
            for coord in ship.coords:
                board.grid[coord[0]-1][coord[1]-1] = "S"
            for hit_coord in ship.hits:
                board.grid[hit_coord[0]-1][hit_coord[1]-1] = "X"
        misses = data.get("misses", [])
        for x in misses:
            board.grid[x[0]-1][x[1]-1] = "O"

        return board
