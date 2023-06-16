# The Guessing Game:

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
        guess = (guess + high)/2
        print(f"Is your secret number {int(guess)}?")
    elif response == 'h':
        high = guess
        guess = (guess + low)/2
        print(f"Is your secret number {int(guess)}?")
print(f"Game over. Your secret numberwas: {int(guess)}")