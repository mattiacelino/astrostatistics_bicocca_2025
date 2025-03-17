import random as rd
from matplotlib import pyplot as plt
import numpy as np

# Mattia Celino 881202
# sorry for the mess !

# generate doors position
def doorGeneration():
    carPosition = rd.randint(0, 2)
    if carPosition == 0:
        return ["car", "goat", "goat"]
    if carPosition == 1:
        return ["goat", "car", "goat"]
    if carPosition == 2:
        return ["goat", "goat", "car"]

# function for the host removing a door
def presentatore(arrayDoors, chosen):
    for d in range(0, 3):
        if d != chosen and arrayDoors[d] == "goat":
            return d #return the index of the removed one

# function for when the player switches door
def switchDoor(removed, chosen):
    for i in range(0, 3):
        if i != removed and i != chosen:
            return i #return the index of the other one

# function that checks the victory
def didWin(doors, chosen):
    if doors[chosen] == "car":
        return True
    else:
        return False

# a single game
def giocatore(arrayDoors, playerName, playerWins):
    # chooses a door
    chosen = rd.randint(0, 2)
    # the host removes one
    removed = presentatore(arrayDoors, chosen)

    # players
    if playerName == "switcher":
        newChosen = switchDoor(removed, chosen)
        if didWin(arrayDoors, newChosen):
            playerWins.append(1)

    if playerName == "conservative":
        if didWin(arrayDoors, chosen):
            playerWins.append(2)

    if playerName == "newcomer":
        del arrayDoors[removed]
        chosen = rd.choice(arrayDoors)
        if chosen == "car":
            playerWins.append(3)

doors = []
switcherWins = []
conservativeWins = []
newcomerWins = []
total = 0

for i in range(0, 2000):
    doors = doorGeneration()
    giocatore(doors, "switcher", switcherWins)
    giocatore(doors, "conservative", conservativeWins)
    giocatore(doors, "newcomer", newcomerWins)
    total += 1

print(total)
print("switcher won ", len(switcherWins), " times (", len(switcherWins)/total, " %)")
print("conservative won ", len(conservativeWins), " times (", len(conservativeWins)/total, " %)")
print("newcomer won ", len(newcomerWins), " times (", len(newcomerWins)/total, " %)")