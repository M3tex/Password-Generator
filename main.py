import secrets
import string
import sys
import time


UPPERCASE, LOWERCASE = string.ascii_uppercase, string.ascii_lowercase
BASIC_SPECIAL_CHARS = "!@#$%^&*()_-+={[}]|\:;'<,>.?/"


def gen_password(n: int, chars=BASIC_SPECIAL_CHARS):
    """Generates a password of length n in a cryptographically safe way.
    
    The password will be composed of at least:
    - One uppercase letter
    - One lowercase letter
    - One number
    - One special character
    """
    if n < 4:
        print("Invalid password length (< 4). Cannot satisfy conditions.")
        print("It is strongly advised to use at least 10 characters")
        sys.exit(1)
    
    initialisation = [UPPERCASE, LOWERCASE, '0123456789', chars]
    password = []

    # We insert characters to be sure that we satisfy the conditions (we'll shuffle later)
    for el in initialisation:
        rdm_idx = secrets.randbelow(len(el))
        password.append(el[rdm_idx])

    while len(password) < n:
        rdm_alphabet = secrets.randbelow(4)
        to_pick_from = initialisation[rdm_alphabet]
        rdm_idx = secrets.randbelow(len(to_pick_from))
        password.append(to_pick_from[rdm_idx])

    # Suffling in a cryptographically safe way
    csprng_shuffle(password)
    return ''.join(password)


def csprng_shuffle(L: list):
    """Shuffles a list in a cryptographically safe way.
    We'll only use the secrets module to generate randomness,
    and the Fisher Yates shuffle.
    """
    for i in range(len(L) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        swap(L, i, j)


def swap(T: list, i: int, j: int):
    tmp = T[i]
    T[i] = T[j]
    T[j] = tmp



if __name__ == "__main__":
    # Getting password length from user
    while True:
        size = input("Password size: ")
        try:
            size = int(size)
        except:
            print("Please enter a number greater than 10.")
            continue
        if size >= 10:
            break
    
    # Getting numbers of passwords to generate
    while True:
        nb = input("Number of passwords: ")
        try:
            nb = int(nb)
        except:
            continue
        if nb > 0:
            break
    
    # Asking user if he wants to specify special characters
    while True:
        special_chars = input("Special characters? (y/n): ")
        if special_chars.lower() == 'y':
            chars = input("Enter wanted special characters: ")
            break
        else:
            chars = BASIC_SPECIAL_CHARS
            break
    
    # Generating passwords
    print("\nYour passwords:\n")
    start = time.time()
    for _ in range(nb):
        print(gen_password(size, chars))
    print()
    end = time.time()
    print(f"{nb} passwords of size {size} generated in: {round(end - start, 2)} seconds")
