from cryptogram import Cryptogram

cryptogram = Cryptogram()
answer, author, category = cryptogram.get_quote()
cipher = cryptogram.build_cipher(answer)

cryptogram.context(author, category)
cryptogram.play(cipher, answer)