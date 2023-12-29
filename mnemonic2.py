import itertools
import subprocess
from datetime import datetime


# 12 słowników - dowolna ilość słów - uwaga im więcej tym dłuzej trwa sprawdzanie
word1 = {'car'}
word2 = {'easy'}
word3 = {'test'}
word4 = {'disagree'}
word5 = {'unit'}
word6 = {'winter'}
word7 = {'pool'}
word8 = {'across'}
word9 = {'dance'}
word10 = {'damp'}
word11 = {'slush'}
word12 = {'priority'}


# Read words from file
print("Reading words from file...")

with open("./words.txt", "r") as file:
    dictionary = file.read().splitlines()

# Check if words from word1 to word12 are in the dictionary
words_lists = [
    word1,
    word2,
    word3,
    word4,
    word5,
    word6,
    word7,
    word8,
    word9,
    word10,
    word11,
    word12,
]

print("Checking if words are in the dictionary...")

for i, words in enumerate(words_lists, start=1):
    print(f"Checking words from word{i}...")
    for word in words:
        print(f"Checking word {word} from word{i}...")
        if word not in dictionary:
            print(f"Word {word} from word{i} is not in the dictionary.")
            exit()

# Generate all possible combinations of 12 words without repetition
print("Generating combinations...")
combinations = itertools.permutations(words_lists, 12)

print("Generated combinations.")

# Execute external program and save the result to a variable
result = ""
for combination in combinations:
    # print(combination)
    # Convert the combination to a string with space-separated words
    # combination_str = " ".join(combination)
    str_tuple = tuple(next(iter(s)) for s in combination)
    mnemonic = " ".join(str_tuple)
    print(mnemonic)

    retries = 3
    while retries > 0:
        try:
            result = subprocess.check_output(
                f"python3 ./exp.py {mnemonic}",
                shell=True,
            )
            output = result.decode("utf-8")
            break
        except subprocess.CalledProcessError:
            print(
                "An error occurred while running the external script. Pausing for 10 seconds..."
            )
            time.sleep(10)
            retries -= 1
    else:
        print(
            "An error occurred three times in a row. Moving to the next combination..."
        )
        continue

    # Check if the result contains "wrong words" and save it to a file
    if "Wrong words!" not in output:
        print("WYNIK: ", output)
        
        # wynik zapisuje do pliku wynik z dopisaniem bieacej daty
        f = open(
            "wynik" + str(datetime.today().strftime("%Y-%m-%d")) + ".txt",
            "a",
        )
        f.write(str(mnemonic) + "\n")
        f.write(str(output) + "\n")
        f.close()
