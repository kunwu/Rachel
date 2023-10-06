import random

while True:
    TheNumber = random.randint(1, 1000)
    print("The number is: " + str(TheNumber))

    character = input("Do you want to play again? (y/n): ")
    if character == "n":
        break