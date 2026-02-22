def shift_key(key: str, text: str) -> str:
    # дз убрать лишние символы из ключа , проверить ключ на 0 символов , проверить если будут только специальные символы

    # убираем лишние символы из текста
    text_without_digits = []
    for char in text:
        if char.isalpha():
            text_without_digits.append(char)
    text = "".join(text_without_digits)
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
