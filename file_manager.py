from ship import Ship
from board import Board
import ast

ship_specs = [
    ("Carrier", 5),
    ("Battleship", 4),
    ("Cruiser", 3),
    ("Submarine", 3),
    ("Destroyer", 2)
]

def save_file(state, filename):
    f = open(filename, "w")
    f.write("Turn: " + state["turn"] + "\n\n")
    f.write("Player 1 Board\n\n")
    for x in state["p1_board"]["ships"]:
        y = ("Ship: " + str(x["name"]) + "\n    Size: " + str(x["size"]) + "\n    Coordinates: " + str(x["coords"]) + "\n    Hits: " + str(x["hits"]) + "\n\n")
        f.write(y)
    f.write("Player 1 Misses: " + str(state["p1_board"]["misses"]) + "\n\n")
    f.write("Player 2 Board\n\n")
    for x in state["p2_board"]["ships"]:
        y = ("Ship: " + str(x["name"]) + "\n    Size: " + str(x["size"]) + "\n    Coordinates: " + str(x["coords"]) + "\n    Hits: " + str(x["hits"]) + "\n\n")
        f.write(y)
    f.write("Player 2 Misses: " + str(state["p2_board"]["misses"]) + "\n")
    f.close()

def load_file(filename):
    f = open(filename, "r")
    lines = f.readlines()
    f.close()
    state = {"p1_board": {"ships": [], "misses": []}, "p2_board": {"ships": [], "misses": []}, "turn": None}
    player = None
    ship_data = None
    for line in lines:
        line = line.strip()
        if not line: continue
        if (line.startswith("Turn: ")):
            state["turn"] = line.split(":")[1].strip()
        elif (line.startswith("Player 1 Board")):
            player = "p1_board"
        elif (line.startswith("Player 2 Board")):
            player = "p2_board"
        elif (line.startswith("Ship: ")):
            if ship_data:
                state[player]["ships"].append(ship_data)
            ship_data = {"name" : line.split(":")[1].strip()}
        elif (line.startswith("Size: ")):
            ship_data["size"] = int(line.split(":")[1].strip())
        elif (line.startswith("Coordinates: ")):
            coords_str = line.split(":")[1].strip()
            ship_data["coords"] = ast.literal_eval(coords_str)
        elif (line.startswith("Hits: ")):
            hits_str = line.split(":")[1].strip()
            ship_data["hits"] = ast.literal_eval(hits_str)
        elif (line.startswith("Player 1 Misses: ")):
            if ship_data:
                state[player]["ships"].append(ship_data)
                ship_data = None
            misses_str = line.split(":")[1].strip()
            state["p1_board"]["misses"] = ast.literal_eval(misses_str)
        elif (line.startswith("Player 2 Misses: ")):
            misses_str = line.split(":")[1].strip()
            state["p2_board"]["misses"] = ast.literal_eval(misses_str)
    if ship_data:
        state[player]["ships"].append(ship_data)
    return state

def load_state(self, filename):
    data = load_file(filename)
    self.p1_board = Board.from_dict(data["p1_board"])
    self.p2_board = Board.from_dict(data["p2_board"])
    self.turn = data["turn"]