# Imports
from math_functions import generate_fibonacci
from math_functions import is_prime
from math_functions import show_prime_range
from math_functions import generate_multiplication_table
from math_functions import calculate_factorial
from math_functions import run_collatz
from math_functions import get_validated_integer


def mathematical_shell():
    """
    Runs main command-line user interface loop for the 
    Number Sequence Analyzer, routing user choices to the 
    appropriate math and logic functions.
    """

    print("Welcome to the Number Sequence Analyer!")


    while True:
        print("\n--- Mathematical Shell ---")
        print("[1] Fibonacci")
        print("[2] Prime Check")
        print("[3] Prime Range")
        print("[4] Multiplication Table")
        print("[5] Factorial")
        print("[6] Collatz")
        print("[7] Exit Program")

        choice = get_validated_integer("Please select an option (1-7): ")

        if choice == 1:
            n = get_validated_integer("Enter how many Fibonacci numbers to generate: ")
            generate_fibonacci(n)

        elif choice == 2:
            n = get_validated_integer("Enter a number to find out if it is prime: ")
            result = is_prime(n)
            print(f"{n} is prime: {result} ")

        elif choice == 3: 
            start = get_validated_integer("Enter the starting number: ")
            end = get_validated_integer("Enter the ending number: ")

            show_prime_range(start, end)

        elif choice == 4:
            n = get_validated_integer("Enter the number for the multiplication table: ")
            length = get_validated_integer("Enter how many rows/lines you want: ")
            generate_multiplication_table(n, length)

        elif choice == 5:
            n = get_validated_integer("Enter a number to get the factorial: ")
            result = calculate_factorial(n)
            print(f"Factorial: {result}")

        elif choice == 6:
            n = get_validated_integer("Enter a number to find the collatz sequence: ")
            result = run_collatz(n)

            if isinstance(result, list):
                steps = len(result) - 1
                print(f"Collatz Sequence: {result}")
                print(f"Steps required: {steps}")
            else:
                print(result)

        elif choice == 7:
            print("\nExiting Program.")
            break

        else:
            print("Invalid choice. Enter a number from 1 to 7.")

if __name__ == "__main__":
    mathematical_shell()