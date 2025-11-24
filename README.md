Battleship – Two-Player Python Game
====================================

A terminal-based implementation of the classic Battleship game.

How it works:
-------------

⦁	On launch you can start a new game or load a save.
⦁	Each player can place ships manually or choose random placement.
⦁	Players take turns firing at coordinates (e.g. D3) until one player's fleet is sunk.
⦁	You can quit during a turn to save the current state and resume later.


The project supports:
---------------------

⦁	two human players
⦁	manual or random ship placement
⦁	coordinate-based firing
⦁	rich-formatted board display
⦁	full save/load functionality through text files.


This README includes:
---------------------

⦁	Project explanation
⦁	Features
⦁	Directory structure
⦁	Setup instructions
⦁	Game instructions


Features
--------

⦁	Two-player Battleship gameplay.
⦁	Manual or random ship placement for each ship.
⦁	Input validation for coordinates and orientations.
⦁	Hit, miss, and sunk-ship detection.
⦁	Colored board display using the 'rich' library.
⦁	Full game state saving to a text file.
⦁	Loading of past games to resume play.
⦁	Support for multiple save files through saves.txt.


Directory Structure
-------------------

Battleship_Project/
├── README.md		   # Read me file for the project
├── board.py          # Board logic: grid, placement, firing, display
├── file_manager.py   # Saving and loading game state
├── game_manager.py   # Game loop, setup, turns, firing logic
├── main.py           # Entry point
└── saves.txt         # Save file list
├── ship.py           # Ship model: coords, hits, sunk check


Setup Instructions
------------------

1.	Install Python:
    
    --> Ensure Python 3.8+ is installed on your system.

2. Install Required Dependency:

    --> The project uses the 'rich' library for colored terminal output:
        pip install rich

3. Ensure that the file "saves.txt" is present the project directory.

4. Run the Game:

    --> From the project directory:
        python main.py


Game Instructions
=================

Starting the Game
-----------------

⦁	When you run main.py, the program asks whether you want to:

   --> Load an existing game, or
   --> Start a new one.

⦁	If you choose to load, available save files (recorded in saves.txt) will be shown.


Ship Placement
--------------

Random Placement:

  Choose 'R' to let the program place ships automatically.

Manual Placement:

  Choose 'M' and provide:
    --> A starting cell (e.g., B7)
    --> An orientation (H or V)

⦁	Invalid inputs or blocked placements will require re-entry.

Taking Turns
------------

Players alternate firing at the opponent’s grid:

1. Enter a coordinate (e.g., D4).

2. The game reports:
   - Hit
   - Miss
   - Ship sunk

3. The board display updates accordingly.


Saving and Quitting
-------------------

⦁	During your firing prompt, type:
    quit

⦁	The game saves:
    --> Both boards
    --> All ship positions and hit states
    --> Missed shots
    --> Current player turn

⦁	Then exits.


Winning
-------

⦁	A player wins when all ships on the opponent’s board are sunk.


Notes
-----

⦁	Save files use a readable text format handled by file_manager.py.
⦁	The structure is modular making it easier to read.
⦁	Compatible with Windows, macOS, and Linux terminals.


Contributors
------------

⦁	Dola Praneeth Kumar Gunda - IE2025012
⦁	Lalith Sai Redroutu - BE2025016
⦁	Yagateela Hemish Sri Chandra - BA2025059
⦁	Siri Mohana - BE2025025
⦁	B.Rithwik - BA2025007

