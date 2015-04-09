import random
import json
import string

class Cryptogram():

    def get_quote(self):
        # Load quotes from text file.
        f = open('quotes.txt', 'r')
        quotes = json.loads(f.read())

        # Get random quote.
        quote = random.choice(quotes)

        # Extract out the quote, author, and category.
        answer = quote['Quote']
        author = quote['Author']
        category = quote['Category']

        # Uppercase the answer and convert to list.
        answer = answer.upper()
        answer = list(answer)

        self.answer = answer
        self.author = author
        self.category = category

    # Build cipher.
    def build_cipher(self):
        # Get uppercase letters into a list.
        alphabet = list(string.uppercase)

        # Get unique letters from original text and location of all occurrences.
        original = []

        for letter in self.answer:
            if letter.isalpha() and letter not in [o['letter'] for o in original]:
                d = {}
                d['letter'] = letter
                d['positions'] = [i for i, x in enumerate(self.answer) if x == letter]
                original.append(d)

        # Copy answer.
        cipher = list(self.answer)

        for o in original:
            # Pick a substitute letter.
            # The substitute can't be the same letter.
            choices = [x for x in alphabet if x != o['letter']]
            sub = random.choice(choices)

            # Remove chosen substitute from choices.
            alphabet.remove(sub)

            for i in o['positions']:
                cipher[i] = sub

        self.cipher = cipher

    def context(self):
        # Show player the author and category.
        print(str(self.author) + " on the category '" + str(self.category) + "'\n")

    def play(self):
        cipher = self.cipher
        answer = self.answer

        # Show player the cipher.
        print(''.join(cipher))

        # Keep track of player's progress.
        progress = list(' ' * len(cipher))

        for i in range(len(cipher)):
            if cipher[i] in string.punctuation:
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
            if before not in cipher:
                print("That letter doesn't exist.")
                continue

            # If player sets RHS letter that is already defined, remove previous definition.
            if after in progress:
                for i in [e for e, x in enumerate(progress) if x == after]:
                    progress[i] = ' '

            for i in [e for e, x in enumerate(cipher) if x == before]:
                # If player doesn't supply RHS letter, remove previous guess.
                if not after:
                    progress[i] = ' '
                # Otherwise, substitute their guess.
                else:
                    progress[i] = after

            # Show player their progress.
            print("".join(progress))
            print("".join(cipher))

            # If the solution has been found, end the game.
            if progress == answer:
                print("\nYay you did it!!!")
                user_input = raw_input("Play again? Y/N ")
                return True if user_input == 'Y' else False
