

def get_validated_integer(prompt):
    """
    Prompt the user for input and continuously loop until a valid integer 
    is provided, catching any ValueError exceptions.
    """

    while True: 

        user_input = input(prompt)

        try:
            return int(user_input)
        
        except ValueError:
            print("Invalid input. Enter a valid whole number")


def generate_fibonacci(n): 
    """
    Generate and print the Fibonacci sequence up to n terms 
    using iterative variable swapping.
    """

    if n <= 0:
        raise ValueError("number must be a positive")

    f,b = 0,1
    for _ in range(n):
       print(f, end=", ")
       
       f,b = b,f+b


def is_prime(n):
    """
    Check whether a given integer is a prime number.
    Returns True if prime, False otherwise.
    """

    if n <= 1:
        return False

    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    
    return True


def show_prime_range(start,end):
    """
    Find and print all prime numbers within the inclusive 
    range from start to end.
    """

    print(f"Prime numbers between {start} and {end}:")

    for n in range(start, end + 1):
        if is_prime(n):
            print(n)


def generate_multiplication_table(n, length):
    """
    Print a multiplication table for a given base number 
    up to the specified table length.
    """

    for i in range(1, length + 1):
        print(f"{n} x {i} = {n * i}")


def calculate_factorial(n):
    """
    Calculate the factorial of a given non-negative integer.
    Returns an error message if the input is negative or None.
    """

    if n is None:
        return "Data unavailable. Please try again"
    
    elif n < 0:
        return "Factorial is not defined for negative numbers"
    
    elif n == 0 or n ==1:
        return 1

    factorial = 1

    for i in range(1,n + 1):
        factorial *= i

    return factorial


def run_collatz(n):
    """
    Generate and return the Collatz sequence list for a given positive integer.
    """

    if n <= 0:
        return "Must be a positive integer"

    sequence = [n]

    while n != 1:
        if n % 2 == 0:
            n = n // 2
        else:
            n = 3* n + 1
        sequence.append(n)

    return sequence