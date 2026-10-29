"""Manages the game logic, state, and scoring rules.
Picks a random target Pokémon from the valid word list.

Validates whether user guesses are valid 5-letter Pokémon.

Compares guesses letter-by-letter to determine green, yellow, or gray feedback.

Tracks remaining turns (e.g., 6 attempts) and victory/loss states."""


# Imports
import random
from api import filter_five_letter_words


def random_secret_word(five_letter_pokemon):
    """Randomly chooses one 5-letter Pokémon from your filtered word 
    list to act as the secret target word for the round."""

    secret_word = random.choice(five_letter_pokemon)

    return secret_word


def validate_player_guess(guess,five_letter_pokemon):
    """Checks if a player's typed input is exactly 5 letters long 
    and exists within the valid Pokémon dictionary. 
    Returns an error message if invalid."""

    try:

        if len(guess) != 5:
            print("Must be exaxtly 5 letters")
            return False
        
        elif  not guess.isalpha():
            print("Must only contain letters")
            return False
        
        elif guess.lower() not in five_letter_pokemon:
            print("Not a valid Pokemon")
            return False
        
        else:
            return True
        
    except ValueError as e:
        print(f"An error has occurred {e} ")


def evaluate_guess_letters(guess,secret_word):
    """Compares the guess letter-by-letter against the secret word to determine which 
    letters are correct (green), misplaced (yellow), or incorrect (gray)."""

    secret_word_list = list(secret_word)

    letter_info = [
        {"letter": "", "status": ""},
        {"letter": "", "status": ""},
        {"letter": "", "status": ""},
        {"letter": "", "status": ""},
        {"letter": "", "status": ""}
    ]

    for i, char in enumerate(guess):
        letter_info[i]['letter'] = char

    for i, pass_1 in enumerate(letter_info):
        if pass_1['letter'] == secret_word_list[i]:
            pass_1['status'] = "green" 
            secret_word_list[i] = None
        
    for i, pass_2 in enumerate(letter_info):

        if pass_2['status'] ==  "green":
            continue
      
        if pass_2['letter'] in secret_word_list:
            pass_2['status'] = "yellow"

            match_idex = secret_word_list.index(pass_2['letter'])
            secret_word_list[match_idex] = None

        else:
            pass_2['status'] = "grey"

    return letter_info


def check_game_status(guess,secret_word,current_attempts):
    """Evaluates whether the player has guessed the word (win), 
    run out of their 6 attempts (loss), or needs to continue to the next turn."""
    
    if guess == secret_word:
        guessed_correct = "You win, you have guessed right!"
        return guessed_correct

    if guess != secret_word and current_attempts == 0:
        no_attempts_left = "You lose, You have run out of attempts"
        return no_attempts_left
    
    return "Continue to next turn" 