def shift_key(key: str, text: str) -> str:
    # убираем лишние символы из ключа
    key_without_digits = []
    for char in text:
        if char.isalpha():
            key_without_digits.append(char)
    key = "".join(key_without_digits)

    # убираем лишние символы из текста
    text_without_digits = []
    for char in text:
        if char.isalpha():
            text_without_digits.append(char)
    text = "".join(text_without_digits)

    # проверяем ключ на 0 символов
    if len(key) == 0:
        print("Ключ состоит из 0 символов, необходимо его заменить")

    # подбираем правильную длину ключа
    if len(key) < len(text):
        extension = len(text) - len(key)
        new_key = key + key[:extension]
    if len(key) > len(text):
        new_key = key[: len(text)]
    return new_key


def encrypt_vigenere_code(text: str, key: str) -> str:
    english_alphabet = "abcdefghijklmnopqrstvupwxyz"
    russia_alphabet = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"


print(shift_key("LEMONFkefjohfeo", "AAA3AAA"))
