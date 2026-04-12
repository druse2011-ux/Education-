class Caesar:
    def __init__(self, shift: int):
        self.shift = shift
        self.english_alphabet = "abcdefghijklmnopqrstvupwxyz"
        self.russia_alphabet = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    
    def _shift_char(self, text: str) -> str:
        list_elements_text = []
        for element in text:
            if element.lower() in self.english_alphabet or element.isalpha() is False:
                if element.islower():
                    new_code = (ord(element) - ord("a") + self.shift) % 26 + ord("a")
                    list_elements_text.append(chr(new_code))
                elif element.isupper():
                    new_code = (ord(element) - ord("A") + self.shift) % 26 + ord("A")
                    list_elements_text.append(chr(new_code))
                else:
                    list_elements_text.append(element)
            elif element.lower() in self.russia_alphabet:
                if element.islower():
                    new_code = (ord(element) - ord("а") + self.shift) % 33 + ord("а")
                    list_elements_text.append(chr(new_code))
                else:
                    new_code = (ord(element) - ord("А") + self.shift) % 33 + ord("А")
                    list_elements_text.append(chr(new_code))
            else:
                break # нужно поменять на raise
        if len(list_elements_text) == len(text):
            return "".join(list_elements_text)
        else:
            raise Exception(
                "Ошибка ввода. Бот принимает текст только на английском или русском языке!"
            )

    def encrypt_caesar_code(self, text: str) -> str:
        return self._shift_char(text)

    def decrypt_caesar_code(self, text: str) -> str:
        self.shift = -self.shift
        result = self.encrypt_caesar_code(text)
        self.shift = -self.shift
        return result


if __name__ == "__main__":
    class_caesar = Caesar(5)
    print(class_caesar)
    print(class_caesar.encrypt_caesar_code("привет!ООАРПРКНРЕНО"))
    print(class_caesar.decrypt_caesar_code("фхнзкч!УУЕХФХПТХКТУ"))
# дз: доделать decrypt, вынести алфавиты в __init__( в аргумент не добавляем)
