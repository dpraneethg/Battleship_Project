from board import Board, alpha_to_num, num_to_alpha
from ship import Ship, notify
from file_manager import save_file, load_state
import sys
import os


""" ship_specs contains ship names and their length ."""

ship_specs = [
    ("Carrier", 5),
    ("Battleship", 4),
    ("Cruiser", 3),
    ("Submarine", 3),
    ("Destroyer", 2)
]

class Game_manager:
    def __init__(self, load, filename, file_names):
        self.filename = filename
        self.p1_board = Board()
        self.p2_board = Board()
        self.turn = "P1"
        self.loaded = load
        self.file_names = file_names
        
        if load == "Y":
            load_state(self, self.filename)
        
        """Loads game from existing file if load is Y. """


    def clear_screen(self):
        """ Clears terminal screen when called."""
        os.system("cls" if os.name == "nt" else "clear")

    def setup_player(self, player_name, board: Board):
        """Seting up players and placing the ships on board manully or randomly based on user input."""
        notify(f"{player_name} Setup", "info")
        choice = input("M For Manual Ship-Placing Glory, Or R To Let The Universe Roll Its Dice: ").strip().upper() or "R"
        self.clear_screen()
        if choice == "M":
            self.manual_place(board, player_name)
        else:
            board.place_random(ship_specs)
        self.clear_screen()
        notify(f"{player_name} Board Ready.", "success")
    
    def manual_place(self, board: Board, player_name):
        """Takes in coordinates and orientation and places the ships if there is no overlapping ships are within the sea range.The user enters maunally."""
        notify("Manual Placement To Give Coordinates. H If You Want Ships To Be Lying Down Or V To Make Ships Stand Tall.", "info")
        for name, size in ship_specs:
            placed = False
            while not placed:
                board.display(player_name, True)
                print(f"Placing {name} (Size {size})")
                pos = input("Starting Cell: ").strip()
                idx = alpha_to_num(pos)
                if not idx:
                    self.clear_screen()
                    notify("Invalid Cell", "error")
                    continue
                orient = input("Orientation (H/V): ").strip().upper()
                if orient not in ("H", "V"):
                    self.clear_screen()
                    notify("It's H Or V, Not Your Face On Keyboard.", "error")
                    continue
                r, c = idx
                ship = Ship(name=name, size=size)
                if board.place_ship(ship, orient, r, c):
                    placed = True
                    self.clear_screen()
                    notify("Placement Success", "success")
                else:
                    self.clear_screen()
                    notify("You Can't Place Ship On Land Or Another Ship. Try Again.", "error")

    def save_state(self, filename):

        """Builds a dict of the full game state and passes it to save_file()."""

        state = {
            "p1_board": self.p1_board.to_dict(),
            "p2_board": self.p2_board.to_dict(),
            "turn": self.turn,
        }
        save_file(state, filename)
    
    def fire(self, attacker_name, target_board):
        """Takes in attacker and target board and coordinates to fire at. Checks whether there is a ship in that coordinate and makes in X or otherwise O for miss.
        If already fired there, it shows the same."""
        while True:
            command = input(f"{attacker_name}, Fire At Coordinate (Ex. D3) Or Type Quit To Quit And Save The Game And Wage War Later: ").strip().upper()
            if not command:
                continue
            if command == "QUIT":
                self.save_state(self.filename)
                if (self.filename not in self.file_names):
                    abcd = open("saves.txt", "a")
                    abcd.write(self.filename + "\n")
                    abcd.close()
                sys.exit()

            index = alpha_to_num(command)
            if not index:
                notify("It's Letter And Number. Not Your Face On Keyboard.", "error")
                continue

            r, c = index
            hit_yes_or_no, sunken_ship = target_board.receive_fire(r, c)

            if hit_yes_or_no is None:
                notify("Already Fired There. You Can't Sink A Sunken Ship Or Water. Try Another.", "error")
                continue

            if hit_yes_or_no:
                self.clear_screen()
                notify(f"Hit At {num_to_alpha(r, c)}!", "success")
                if sunken_ship:
                    notify(f"Sank {sunken_ship}! Congratulations, You Killed Hundreds.", "success")
            else:
                self.clear_screen()
                notify(f"Miss At {num_to_alpha(r, c)}. Waste Of Missile.", "warning")

            break

    def loop(self):
        """This is where the game loop method is made.
        If loaded is Y ,then players are already setup. If loaded is N, then setup_player is called to setup two players.
        Then the loop starts. Turn is shifted between the 2 players till either one player's ships are all sunk."""
        notify("Two Player Battleship Game Starts", "info")
        if (self.loaded == "N"):
            self.setup_player("Player 1", self.p1_board)
            self.setup_player("Player 2", self.p2_board)

        while True:
            attacker = "Player 1" if self.turn == "P1" else "Player 2"
            defender = "Player 2" if self.turn == "P1" else "Player 1"
            target_board = self.p2_board if self.turn == "P1" else self.p1_board

            notify(f"{attacker}'s Turn.", "info")
            if self.turn=="P1":
                self.p2_board.display("P2 Board")
            else:
                self.p1_board.display("P1 Board")
            notify(f"{defender}'s Board (Your Hits Shown):", "info")

            

            self.fire(attacker, target_board)
            if self.turn=="P1":
                self.p2_board.display("P2 Board")
            else:
                self.p1_board.display("P1 Board")
            if target_board.all_sunk():
                notify(f"All Ships Of {defender} Are Sunk! {attacker} Wins! Congratulations, You Colonized {defender}'s Ocean.", "success")
                break

            input("\nPress Enter And Pass The Ability To Kill To Your Enemy...")
            self.clear_screen()
            self.turn = "P2" if self.turn == "P1" else "P1"


