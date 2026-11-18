
# Imports

import re
import random
from api_handler import WordPieceManager


# Game Logic


class WordPieceEngine:
    """Encapsulates the core game logic and comparison mechanics for 
    the One Piece Wordle guessing game."""

    @staticmethod
    def random_secret_character(all_characters):
        """Selects and returns a random secret target character 
        from a validated list of available character dictionaries."""

        valid_characters = [
        char for char in all_characters if (
            char is not None
            and char.get('age') is not None
            and char.get('height') is not None
            and char.get('bounties') is not None

            )
        ]

        # print(f"Valid characters: {len(valid_characters)}")

        if not valid_characters:
            return None

        secret_character = random.choice(valid_characters)
        return secret_character

    @staticmethod
    def attribute_comparison_tool(guess,secret_character):
        """Compares a player's character guess against the secret target character 
        across multiple attributes (age, height, first appearance, bounties, affiliation, 
        and devil fruits) and returns a structured feedback dictionary with directional clues."""

        feedback = {}

        if guess['name'] == secret_character['name']:
            feedback['name'] = {'name': guess['name'],'status': 'exact', 'clue': 'Match🎯' }
        
        else:
            feedback['name'] = {'name': guess['name'],'status': 'mismatch', 'clue': 'X'}


        if guess['age'] is None or secret_character['age'] is None:
            feedback['age'] = {'status': 'error', 'clue': 'Data Unavailable' }
        elif guess['age'] == secret_character['age']:
            feedback['age'] = {'status': 'exact', 'clue': 'Match🎯' }
        elif guess['age'] < secret_character['age']:
            feedback['age'] = {'status': 'higher', 'clue': 'Higher ↑' }
        elif guess['age'] > secret_character['age']:
            feedback['age'] = {'status': 'lower', 'clue': 'Lower ↓' }
            
                
        if guess['height'] is None or secret_character['height'] is None:
            feedback['height'] = {'status': 'error', 'clue': 'Data Unavailable' }
        elif guess['height'] == secret_character['height']:
            feedback['height'] = {'status': 'exact', 'clue': 'Match🎯' }
        elif guess['height'] < secret_character['height']:
            feedback['height'] = {'status': 'higher', 'clue': 'Higher ↑' }
        elif guess['height'] > secret_character['height']:
            feedback['height'] = {'status': 'lower', 'clue': 'Lower ↓' }
    
    
        if guess['first_appearance'] is None or secret_character['first_appearance'] is None:
            feedback['first_appearance'] = {'status': 'error', 'clue': 'Data Unavailable' }
        elif guess['first_appearance'] == secret_character['first_appearance']:
            feedback['first_appearance'] = {'status': 'exact', 'clue': 'Match🎯' }
        elif guess['first_appearance'] < secret_character['first_appearance']:
            feedback['first_appearance'] = {'status': 'higher', 'clue': 'Higher ↑' }
        elif guess['first_appearance'] > secret_character['first_appearance']:
            feedback['first_appearance'] = {'status': 'lower', 'clue': 'Lower ↓' }

            
        if guess['bounties'] is None or secret_character['bounties'] is None:
            feedback['bounties'] = {'status': 'error', 'clue': 'Data Unavailable' }
        elif guess['bounties'] == secret_character['bounties']:
            feedback['bounties'] = {'status': 'exact', 'clue': 'Match🎯' }
        elif guess['bounties'] < secret_character['bounties']:
            feedback['bounties'] = {'status': 'higher', 'clue': 'Higher ↑' }
        elif guess['bounties'] > secret_character['bounties']:
            feedback['bounties'] = {'status': 'lower', 'clue': 'Lower ↓' }


        if guess['affiliation'] is None or secret_character['affiliation'] is None:
            feedback['affiliation'] = {'status': 'error', 'clue': 'Data Unavailable' }
        elif guess['affiliation'] == secret_character['affiliation']:
            feedback['affiliation'] = {'status': 'exact', 'clue': 'Match🎯'}
        else:
            feedback['affiliation'] = {'status': 'incorrect', 'clue': 'X'}


        if guess['devil-fruits'] is None or secret_character['devil-fruits'] is None:
            feedback['devil-fruits'] = {'status': 'error', 'clue': 'Data Unavailable' }
        elif guess['devil-fruits'] == secret_character['devil-fruits']:
            feedback['devil-fruits'] = {'status': 'exact', 'clue': 'Match🎯' }
        else:
            feedback['devil-fruits'] = {'status': 'incorrect', 'clue': 'X' }


        return feedback             