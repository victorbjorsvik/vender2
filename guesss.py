print("Please think of a number between 0 and 100!")

print("Is your secret number 50?")

low = 0
guess = 50
high = 100
response = ""

while response != 'c':
    response = input("Enter 'h' to indicate the guess is too high. Enter 'l' to indicate the guess is too low. Enter 'c' to indicate I guessed correctly. ")
    if response == 'l':
        low = guess
        guess = int((guess + high)/2)
        print("Is your secret number " + str(guess) + "?")
    elif response == 'h':
        high = guess
        guess = int((guess + low)/2)
        print("Is your secret number " + str(guess) + "?")
    elif response == 'c':
        break
    else:
        print("Sorry, I did not understand your input.")
        print("Is your secret number " + str(guess) + "?")

print("Game over. Your secret number was: " + str(guess))