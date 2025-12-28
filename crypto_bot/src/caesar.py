def encrypt_caesar_code(text: str, shift: int) -> str:
    english_alphabet = "abcdefghijklmnopqrstvupwxyz"
    russia_alphabet = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    list_elements_text = []
    for element in text:
        if element.lower() in english_alphabet or element.isalpha() is False:
            if element.islower():
                new_code = (ord(element) - ord("a") + shift) % 26 + ord("a")
                list_elements_text.append(chr(new_code))
            elif element.isupper():
                new_code = (ord(element) - ord("A") + shift) % 26 + ord("A")
                list_elements_text.append(chr(new_code))
            else:
                list_elements_text.append(element)
        elif element.lower() in russia_alphabet:
            if element.islower():
                new_code = (ord(element) - ord("а") + shift) % 33 + ord("а")
                list_elements_text.append(chr(new_code))
            else:
                new_code = (ord(element) - ord("А") + shift) % 33 + ord("А")
                list_elements_text.append(chr(new_code))
        else:
            break
    if len(list_elements_text) == len(text):
        return "".join(list_elements_text)
    else:
        return (
            "Ошибка ввода. Бот принимает текст только на английском или русском языке!"
        )


def decrypt_caesar_code(text: str, shift: int) -> str:
    return encrypt_caesar_code(text, -shift)


if __name__ == "__main__":
    print(encrypt_caesar_code("привет!ООАРПРКНРЕНО", 5))
    print(decrypt_caesar_code("фхнзкч!УУЕХФХПТХКТУ", 5))
