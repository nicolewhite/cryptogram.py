from cryptogram import Cryptogram

cryptogram = Cryptogram()

play_again = True

while play_again:
    cryptogram.get_quote()
    cryptogram.build_cipher()
    cryptogram.context()
    play_again = cryptogram.play()

print("Thanks for playing.")