from src.cipher import Cipher

class Vignure(Cipher):
    def __init__(self, shift: int):
        self.shift = shift
        self.english_alphabet = "abcdefghijklmnopqrstvupwxyz"
        self.russia_alphabet = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    
    def clean_string_key_and_text(value: str) -> str:
        # убирает все небуквенные символы
        return "".join([char for char in value if char.isalpha()])


    def extand_key(key: str, text: str) -> str:
        # проверяет правильное ли количество символов у ключа и расширяет при необходимости
        if len(key) == 0:
            # позже необходимо сделать исключение
            return "Ключ состоит из 0 символов, необходимо его заменить"
        if len(key) < len(text):
            extension = len(text) - len(key)
            new_key = key + key[:extension]
        if len(key) > len(text):
            new_key = key[: len(text)]
        return new_key


    def shift_key(key: str, text: str) -> str:
        # тут хранится готовый ключ
        key = self.clean_string_key_and_text(key)
        text = self.clean_string_key_and_text(text)
        return self.extand_key(key, text)


    def _encrypt_vigenere_code(text: str, key: str) -> str:
        english_alphabet = "abcdefghijklmnopqrstvupwxyz"
        russia_alphabet = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
        new_key = self.shift_key(key, text)
        index_key = []
        index_text = []
        answer = []
        for char in new_key.lower():
            if char in english_alphabet:
                index_key.append(english_alphabet.index(char))
            elif char in russia_alphabet:
                index_key.append(russia_alphabet.index(char))
            else:
                print("Бот работает только с русскими и английскими символами")

        for char in text.lower():
            if char in english_alphabet:
                index_text.append(english_alphabet.index(char))
            elif char in russia_alphabet:
                index_text.append(russia_alphabet.index(char))
            elif not char.isalpha():
                index_text.append(char)
            else:
                print("Бот работает только с русскими и английскими символами")

        if any(char in english_alphabet for char in text.lower()):
            alphabet = english_alphabet
        else:
            alphabet = russia_alphabet
        key_position = 0
        for char in index_text:
            if isinstance(char, str):
                answer.append(char)
            else:
                new_index = (char + index_key[key_position]) % len(alphabet)
                answer.append(alphabet[new_index])
                key_position += 1
        return "".join(answer)

if __name__ == "__main__":
    class_vignure = Vignure(5)
    print(class_vignure)
    print(class_vignure.encrypt_vignure_code("привет!ООАРПРКНРЕНО"))
    print(class_vignure.decrypt_vignure_code("фхнзкч!УУЕХФХПТХКТУ"))

