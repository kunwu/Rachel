import random

print("Guess a number between 1 and 1000")

TheNumber = random.randint(1, 1000)

while True:
    guess = int(input("Enter your guess: "))
    if guess == TheNumber:
        print("You guessed it right!")
        break
    elif guess > TheNumber:
        print("Your guess is too high")
    else:
        print("Your guess is too low")