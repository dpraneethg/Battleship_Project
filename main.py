from game_manager import Game_manager
from game_manager import notify
import os

os.system("cls" if os.name == "nt" else "clear")
notify("Namaste Beloved TAs. 🙏", "info")
notify("Choose Wisely, Adventurer. 'Y' Restores Thy Glory, 'N' Makes Thee A Peasant Once More.", "info")

while True:
    load = input("Do Thou Want To Load Existing Game (Y/N): ").upper()
    os.system("cls" if os.name == "nt" else "clear")
    fle = open("saves.txt", "r")
    line_all = fle.readlines()
    fle.close()
    file_names = [] 
    for x in line_all:
        file_names.append(str(x.strip()))
    if (load == "Y" and len(file_names) > 0):
        names = []
        for i in file_names:
            names.append(i.split(".")[0])
        notify(", ".join(names), "info")
        filename = input("Choose A Save File: ").lower() + ".txt"
        while (filename not in file_names):
            notify("Invalid File Name.", "error")
            filename = input("Choose A Save File: ").lower() + ".txt"
        notify("🌊 The Ocean Awaits... And So Do Enemy Torpedoes. Good Luck, Sailor!", "success")
        input("Press Enter To Start.")
        gm = Game_manager(load, filename, file_names)
        gm.loop()
        break
    elif (load == "Y" and len(file_names) == 0):
        notify("⚓ You Tried To Load A Save... But The Only Thing Saved Is Disappointment.", "error")
        continue
    elif (load == "N"):
        filename = input("Enter The Name Of The File You Want To Save Your Game In: ")
        filename += ".txt"
        gm = Game_manager(load, filename, file_names)
        gm.loop()
        break
    else:
        notify("💥 Wrong Command. If You Steer Your Fleet Like You Type, We're Doomed Already. Type Y Or N", "error")
        continue



