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
    key = clean_string_key_and_text(key)
    text = clean_string_key_and_text(text)
    return extand_key(key, text)


def encrypt_vigenere_code(text: str, key: str) -> str:
    english_alphabet = "abcdefghijklmnopqrstvupwxyz"
    russia_alphabet = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    new_key = shift_key(key, text)
    index_key = []
    index_text = []
    answer = []
    for char in new_key.lower():
        if char in english_alphabet:
            index_key.append(english_alphabet.index(char))
        elif char in russia_alphabet:
            index_key.append(russia_alphabet.index(char))
        else:
            # позже необходимо сделать исключение
            return "бот работает только с русскими и английскими символами"

    for char in text.lower():
        if char in english_alphabet:
            index_text.append(english_alphabet.index(char))
        elif char in russia_alphabet:
            index_text.append(russia_alphabet.index(char))
        elif not char.isalpha():
            index_text.append(char)
        else:
            # позже необходимо сделать исключение
            return "бот работает только с русскими и английскими символами"
    # переделать код и доюавить алфавиты ( узнать какой алфавит) и брать остаток от деления алфавита
    for char in range(len(index_text)):
        if isinstance(index_text[char], str):
            answer.append(index_text[char])
        else:
            if char >= len(index_key):
                break
            else:
                answer.append(english_alphabet[index_text[char] + index_key[char]])
    print(answer)


print(encrypt_vigenere_code("AAA3AAA", "LEMONFkefjohfeo"))
