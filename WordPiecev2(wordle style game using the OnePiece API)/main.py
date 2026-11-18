
# Imports

from api_handler import WordPieceManager
from api_handler import normalize_value
from game import WordPieceEngine
from rich.console import Console
from rich.table import Table
from InquirerPy import inquirer
from prompt_toolkit.completion import FuzzyWordCompleter
import sys




class WordPiece:
    """It acts as the primary orchestrator, maintaining round states, 
    delegating attribute comparisons to the engine, processing input loops, and managing terminal UI rendering."""


    def __init__(self):
        self.guess_history = []
        self.guess_total = 0
        self.console = Console()


    def play_round(self,all_characters, completer):
        """Executes a single, complete round of Word Piece.

        Selects a random target character, resets guess tracking, processes player 
        input via InquirerPy, evaluates attribute feedback, and renders the comparison 
        table until the player guesses correctly or exits."""

        secret_character = WordPieceEngine.random_secret_character(all_characters)

        self.guess_history = []
        self.guess_total = 0
        
        self.console.print("(type exit or quit to leave game)")

        while True:
        
            guess = inquirer.text(
                message="Type A One Piece Character: ",
                completer=completer,
                multicolumn_complete=False,
                amark="✔"
            ).execute()
        
            if guess in ['exit', 'quit']:
                self.console.print("Thank you for playing")
                self.console.print(f" The One Piece Character was {secret_character['name']}")
                return False

            matched_character = None
            
            for scan in all_characters:
                         
                if guess.lower() == scan['name'].lower():
                    matched_character = scan
                    break
            
            
            if matched_character is not None:

                self.guess_total += 1

                feedback_result = WordPieceEngine.attribute_comparison_tool(matched_character, secret_character)
                self.guess_history.append(feedback_result)

                self.display_terminal()
                                    
                if matched_character['name'].lower() == secret_character['name'].lower():
                    self.console.print(f"You win, you have guessed: {secret_character['name']}")
                    self.console.print(f"Total guesses: {self.guess_total}")

                    while True:
                                    
                        choice = self.console.input("Do you want to play again(y/n): ").strip().lower()
                                    
                        if choice in ['yes','y']:
                            return True
                                    
                        elif choice in ['no','n']:
                            self.console.print("Thank you for playing")
                            return False
                                    
                        else: 
                            self.console.print("Invalid value, try again")
                                    
            else:
                self.console.print("Please try again, Character is not valid")


    def game_loop(self):
        """Manages the application lifecycle and replay loop.

        Pre-loads the character dataset and autocomplete engine once at startup, 
        then continuously triggers individual game rounds via play_round until 
        the player chooses to exit.
        """

        all_characters = WordPieceManager.cache_manager()
        
        all_names = WordPieceManager.fetch_character_name_list()

        completer = FuzzyWordCompleter(all_names)


        while True:
            play_again = self.play_round(all_characters,completer)

            if not play_again:
                break


    def clear_screen(self):
        """Clears terminal.

        Addresses VS Code integrated terminal scrollback buffer behavior"""

        self.console.clear()

        sys.stdout.write("\033[3J")
        sys.stdout.flush()

              
    def display_terminal(self):
        """Renders the current guess history and directional attribute clues 
        inside a formatted Rich terminal grid."""

        self.clear_screen()

        table = Table(title="WORD PIECE", show_lines=True)

        table.add_column("Character Name", justify="center")
        table.add_column("Age", justify="center")
        table.add_column("Height",justify="center")
        table.add_column("First Appearance", justify="center")
        table.add_column("Bounty", justify="center")
        table.add_column("Affiliation", justify="center")
        table.add_column("Devil Fruit",justify="center")


        for guesses in self.guess_history:
            guessed_name = guesses.get('name')
            age = guesses['age']
            height = guesses['height']
            first_appearance = guesses['first_appearance']
            bounties = guesses['bounties']
            affiliation = guesses['affiliation']
            devil_fruits = guesses['devil-fruits']
            
            age_clue = age.get('clue')
            height_clue = height.get('clue')
            first_appearance_clue = first_appearance.get('clue')
            bounties_clue = bounties.get('clue')
            affiliation_clue = affiliation.get('clue')
            devil_fruits_clue = devil_fruits.get('clue')

            try:
                table.add_row(
                    guessed_name['name'],
                    age_clue,
                    height_clue,
                    first_appearance_clue,
                    bounties_clue,
                    affiliation_clue,
                    devil_fruits_clue
                    )
            except Exception as e:
                self.console.print(f"Table error: {e}")

        self.console.print(table)
        self.console.print(f"Total Guesses: {self.guess_total}")   
        self.console.print("(type exit or quit to leave game)")        
    

def main():
    """Initializes and launches the Word Piece game instance."""

    word_piece_instance = WordPiece()
    word_piece_instance.game_loop()
    

if __name__ == "__main__":
    main()