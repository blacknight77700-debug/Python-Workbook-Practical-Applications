"""The entry point you run to play the game.
Displays introductory welcome messages and instructions.

Accepts player input from the terminal.

Formats feedback in the terminal (using colored text/backgrounds for green, yellow, and gray).

Runs the main game loop until the player wins or runs out of turns."""

# Imports
import colorama, rich
from colorama import Fore, Back, Style
from rich import table
from game import check_game_status
from game import evaluate_guess_letters
from game import validate_player_guess
from game import random_secret_word



def display_welcome_banner():
    """Prints the game title, introductory instructions, 
    and rules to the terminal when the app starts."""
    
    print("\n--- WHO'S THAT WORDLE---")
    print("How to Play")
    print("Guess the Pokemon in 6 attempts")
    print("* Each guess must be a valid 5-letter pokemon")
    print("* The color of the tiles will change to show how close your guess was to the pokemon")
    print("[1] Go play")

    choice = input("Please select option 1 to play")

    if choice == "1":
        print("Go Play")
        return


def render_colored_guess(letter_info):
    """Takes the letter evaluation results and prints them in the terminal 
    using color coding (green backgrounds, yellow backgrounds, gray backgrounds)."""

    for ren in letter_info:
        if ren['status'] == "green":
            print(Back.GREEN + Fore.WHITE +  ren['letter'] + Style.RESET_ALL, end="")

        if ren['status'] == "yellow":
            print(Back.YELLOW + Fore.WHITE +  ren['letter'] + Style.RESET_ALL, end="")

        if ren['status'] == "grey":
            print(Back.LIGHTBLACK_EX + Fore.WHITE +  ren['letter'] + Style.RESET_ALL, end="")


def run_game_loop(secret_word):
    """Controls the core turn-by-turn progression—prompting the user for input, validating it, 
    updating the screen feedback, and checking for win/loss conditions."""

    attempts_left = 6

    while True:
        guess = input("Enter a 5-letter pokemon: ")

        validated_guess = validate_player_guess(guess)

        if  not validated_guess:
            print("Invalid guess, try again")
            continue


        evaluated_guess = evaluate_guess_letters(guess, secret_word)
        render_colored_guess(evaluated_guess)

        attempts_left -= 1
        print(f"Attempts left: {attempts_left}")

        status = check_game_status(guess,secret_word,attempts_left)

        if status == "You win, you have guessed right!":
            print(status)
            break

        if status == "You lose, You have run out of attempts":
            print(status)
            print(f"The secret Pokemon is {secret_word}")
            break


def main():
    """The primary entry point script that initializes the app, calls the game loop, and asks the player 
    if they want to play again once a round ends."""

    display_welcome_banner()

    while True:
        secret_word = random_secret_word()

        run_game_loop(secret_word)

        while True:
            choice = input("Do you want to play again(y/n): ").strip().lower()

            if choice in ['yes','y']:
                break

            elif choice in ['no','n']:
                print("Thank you for playing")
                return

            else: 
                print("Invalid value, try again")


if __name__ == "__main__":
    main()