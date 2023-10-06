import random

while True:
    Digict1 = random.randint(1, 9)
    Digict2 = random.randint(1, 9)
    Digict3 = random.randint(1, 9)
    Digict4 = random.randint(1, 9)

    TheNumber = Digict1 * 1000 + Digict2 * 100 + Digict3 * 10 + Digict4
    print("The number is: " + str(TheNumber))

    character = input("Do you want to play again? (y/n): ")
    if character == "n":
        break