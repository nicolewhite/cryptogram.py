import random
import json
import string

class Cryptogram():
    def get_quote(self):
        f = open('quotes.txt', 'r')
        quotes = json.loads(f.read())
        quote = random.choice(quotes)

        answer = quote['Quote']
        author = quote['Author']
        category = quote['Category']

        return(answer, author, category)

    # Build cipher.
    def build_cipher(self, answer):
        answer = answer.upper()
        answer = list(answer)

        # Get uppercase letters into a list.
        alphabet = list(string.uppercase)

        # Get unique letters from original text and location of all occurrences.
        original = []

        for letter in answer:
            if(letter.isalpha() and letter not in [o['letter'] for o in original]):
                d = dict()
                d['letter'] = letter
                d['positions'] = [i for i, x in enumerate(answer) if x == letter]
                original.append(d)

        # Copy answer.
        cipher = list(answer)

        for o in original:
            # Pick a substitute letter.
            # The substitute can't be the same letter.
            choices = [x for x in alphabet if x != o['letter']]
            sub = random.choice(choices)

            # Remove chosen substitute from choices.
            alphabet.remove(sub)

            for i in o['positions']:
                cipher[i] = sub

        return(cipher)

    def context(self, author, category):
        # Show player the author and category.
        print(str(author) + " on the category '" + str(category) + "'\n")

    def play(self, cipher, answer):
        # Show player the cipher.
        print("".join(cipher))

        # Keep track of player's progress.
        progress = list(" " * len(cipher))

        for i in range(len(cipher)):
            if(cipher[i] in string.punctuation):
                progress[i] = cipher[i]

        while True:
            user_input = raw_input("Take a guess: ")

            # Player guesses in the form "A = B".
            try:
                before = user_input.split('=')[0].replace(' ', '').upper()
                after = user_input.split('=')[1].replace(' ', '').upper()
            except:
                print("Check your syntax. Your guesses should be in the form 'letter = letter', e.g. 'R = T'.")
                continue

            # If player sets LHS letter that isn't in the puzzle, move on.
            if(before not in cipher):
                print("That letter doesn't exist.")
                continue

            # If player sets RHS letter that is already defined, remove previous definition.
            if(after in progress):
                for i in [e for e, x in enumerate(progress) if x == after]:
                    progress[i] = ' '

            for i in [e for e, x in enumerate(cipher) if x == before]:
                # If player doesn't supply RHS letter, remove previous guess.
                if(after == ''):
                    progress[i] = ' '
                # Otherwise, substitute their guess.
                else:
                    progress[i] = after

            # Show player their progress.
            print("".join(progress))
            print("".join(cipher))

            # If the solution has been found, end the game.
            if(progress == answer):
                print("Yay you did it!!!")
                return()
