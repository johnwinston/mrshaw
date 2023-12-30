from ascii_art import mrshaw
import itertools
import os
from tqdm import tqdm

def get_user_confirmation(prompt):
    return input(prompt).lower() == "y"

def save_to_file(content, filename):
    try:
        with open(filename, "w") as f:
            f.write(content)
        print(f"File saved as {filename}")
    except IOError as e:
        print("Error saving file: {e}")

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def find_singular_prime(n):
    from sympy import isprime
    found = False
    if isprime(n):
        print("Number is prime!")
        print("Saving prime to file...")
        #filename = input("Enter filename: ")
        save_to_file(str(n), "mrshaw_prime.txt")
        found = True
    return found

def find_prime(n):
    from sympy import isprime
    print("Finding prime...")

    number = n + (1 if n % 2 == 0 else 0)
    attempts = 0

    prime = False
    while not prime:
        number = number + 2 if number % 5 == 0 else number

        prime = isprime(number)
        if prime:
            print("\nNumber is prime!")
            print("Saving prime to file...")
            filename = input("Enter filename: ")
            save_to_file(str(number), filename)
        else:
            number = number + 2 
            attempts = attempts + 1
            print(f"\rOh no.. {attempts} attempts failed.", end='')
    return number

def convert_art_to_numbers(ascii_art):
    print("Replacing characters with numbers...")
    numbers = ""
    for letter in ascii_art:
        if letter == " ":
            numbers += "1"
        elif letter == "\n":
            numbers += "\n"
        else:
            numbers += "8"
    return numbers

def number_to_art(number):
    for i, char in enumerate(number):
        if i % 163 == 0:
            print()
        else:
            print(char, end="")

def matrix_to_art(matrix):
    art = ""
    for row in matrix:
        for char in row:
            art += char
        art += "\n"
    art = art[:-1]  # Remove the last newline
    return art

import copy

def replace_numbers_with_coords(matrix, coords):
    new_matrix = copy.deepcopy(matrix)  # Create a copy of the matrix
    for coord in coords:
        i,j = coord
        if new_matrix[i][j] == "8":
            new_matrix[i][j] = "1"
        elif new_matrix[i][j] == "1":
            new_matrix[i][j] = "8"
    return new_matrix

def generate_permutations(original_matrix, groups):
    permutations = []
    for group in groups:
        permuted_matrix = replace_numbers_with_coords(original_matrix, group)
        permutations.append(permuted_matrix)
    return permutations

def generate_combinations(original_matrix, groups):
    all_combinations = []

    total_combinations = sum(1 for r in range(1, len(groups) + 1) for _ in itertools.combinations(groups, r))

    with tqdm(total=total_combinations, desc="Generating combinations") as pbar:
        for r in range(1, len(groups) + 1):
            for subset in itertools.combinations(groups, r):
                flattened_coords = [coord for group in subset for coord in group]
                combined_matrix = replace_numbers_with_coords(original_matrix, flattened_coords)
                all_combinations.append(combined_matrix)
                pbar.update(1)  # Update the progress bar

    return all_combinations

def read_and_group_coordinates(file_path):
    import csv
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        groups = []
        current_group = []
        next(reader)  # Skip the first row

        for row in reader:
            if row:  # if the row is not empty
                current_group.append((int(row[0]), int(row[1])))
            else:  # if the row is empty
                if current_group:  # if there's something in the current group
                    groups.append(current_group)
                    current_group = []

        if current_group:  # Add the last group if not empty
            groups.append(current_group)

        return groups

def matrix_to_numbers(matrix):
    numbers = ""
    for row in matrix:
        for char in row:
            numbers += char
    return numbers
        
def main():
    with open("mrshaw_prime.txt", "r") as f:
        numbers = f.read()
    from sympy import isprime
    print(len(numbers))
    #number = int(numbers)
    #if isprime(number):
    #    print("Number is prime!")

    number_to_art(numbers)
    print()
    '''
    with open("mrshaw.txt", "r") as f:
        numbers = f.read()
    coords = read_and_group_coordinates("coords.csv")

    # Convert numbers to matrix
    numbers = numbers.split("\n")
    numbers = [list(row) for row in numbers]
    numbers = [row for row in numbers if row != []]

    #coords = coords[0:1]

    combinations = generate_combinations(numbers, coords)
    for c in tqdm(combinations):
        result = matrix_to_art(c)
        print(result)
        numbers = matrix_to_numbers(c)
        found = find_singular_prime(int(numbers.replace("\n", "")))
        if found:
            break
    '''

    #permutations = generate_permutations(numbers, coords)
    #for p in permutations:
    #    print(matrix_to_art(p))
    #    numbers = matrix_to_numbers(p)
    #    number = find_singular_prime(int(numbers.replace("\n", "")))
    return
    number = numbers.replace("\n", "")

    number = find_prime(int(numbers.replace("\n", "")))
    ascii_art = mrshaw
    print(f"ASCII Art:\n{ascii_art}")
    if get_user_confirmation("Convert art to numbers? (Y/N) "):
        numbers = convert_art_to_numbers(ascii_art)
        print(f"Numbers:{numbers}")

        if get_user_confirmation("Do you want to save it as a file? (Y/N) "):
            filename = input("Enter filename: ")
            save_to_file(numbers, filename)

    if get_user_confirmation("Do you want to find a prime? (Y/N) "):
        if get_user_confirmation("Do you want to import the prime number? (Y/N) "):
            filename = input("Enter filename: ")
            with open(filename, "r") as f:
                numbers = f.read()
        number = find_prime(int(numbers.replace("\n", "")))
        print(f"Prime number: {number}\nLength: {len(str(number))}")

if __name__ == "__main__":
    main()
