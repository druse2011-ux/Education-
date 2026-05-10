"""
vigenere.py

Класс шифра Виженера
для подключения к GUI приложению.

Интерфейс такой же как у CaesarCipher:

encrypt()
decrypt()

Это важно, потому что UI
должен одинаково работать
с разными алгоритмами.
"""
from src.cipher import Cipher
# =========================================================
# АЛФАВИТЫ
# =========================================================

# Английский алфавит
EN_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# Русский алфавит
RU_ALPHABET = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"


# =========================================================
# КЛАСС ШИФРА ВИЖЕНЕРА
# =========================================================

class VigenereCipher(Cipher):

    """
    Шифр Виженера.

    Работает через ключ:

    ТЕКСТ + КЛЮЧ

    Пример:

    TEXT:
    ATTACKATDAWN

    KEY:
    LEMONLEMONLE

    Каждая буква текста
    сдвигается на значение
    буквы ключа.
    """

    def __init__(self, key: str):

        # Проверяем что ключ не пустой

        if not key:
            raise ValueError(
                "Ключ не может быть пустым"
            )

        # Сохраняем ключ
        self.key = key.upper()

    # =====================================================
    # ВСПОМОГАТЕЛЬНЫЕ МЕТОДЫ
    # =====================================================

    def _get_alphabet(self, text: str):

        """
        Определяем какой алфавит использовать.

        Если нашли русскую букву →
        используем русский алфавит.

        Иначе английский.
        """

        for ch in text.upper():

            if ch in RU_ALPHABET:
                return RU_ALPHABET

        return EN_ALPHABET

    def _validate_key(self, alphabet):

        """
        Проверяем что ключ
        содержит только символы
        выбранного алфавита.
        """

        for ch in self.key:

            if ch not in alphabet:

                raise ValueError(
                    f"Недопустимый символ в ключе: {ch}"
                )

    def _shift_char(
        self,
        text_char,
        key_char,
        alphabet,
        encrypt=True
    ):

        """
        Шифрование ОДНОГО символа.

        Это инкапсуляция:

        encrypt() не знает
        как двигаются буквы.

        Он просто вызывает:

        _shift_char()
        """

        alphabet_size = len(alphabet)

        # Индекс буквы текста
        text_index = alphabet.index(
            text_char
        )

        # Индекс буквы ключа
        key_index = alphabet.index(
            key_char
        )

        # -----------------------------------------
        # Шифрование
        # -----------------------------------------

        if encrypt:

            new_index = (
                text_index + key_index
            ) % alphabet_size

        # -----------------------------------------
        # Дешифрование
        # -----------------------------------------

        else:

            new_index = (
                text_index - key_index
            ) % alphabet_size

        return alphabet[new_index]

    # =====================================================
    # ОСНОВНАЯ ЛОГИКА
    # =====================================================

    def _process(
        self,
        text,
        encrypt=True
    ):

        """
        Общая логика:

        encrypt()
        decrypt()

        используют один и тот же метод.
        """

        alphabet = self._get_alphabet(
            text
        )

        # Проверяем ключ
        self._validate_key(alphabet)

        text = text.upper()

        result = []

        # Индекс ключа
        key_index = 0

        for ch in text:

            # Если символ буква
            if ch in alphabet:

                # Зацикливаем ключ:

                # KEYKEYKEYKEY

                current_key_char = self.key[
                    key_index % len(self.key)
                ]

                result.append(

                    self._shift_char(
                        ch,
                        current_key_char,
                        alphabet,
                        encrypt
                    )
                )

                # Двигаем ключ
                # только на буквах

                key_index += 1

            else:

                # Пробелы и символы
                # не шифруем

                result.append(ch)

        return "".join(result)

    # =====================================================
    # PUBLIC API
    # =====================================================

    def encrypt(self, text):

        """
        Публичный метод шифрования.
        """

        return self._process(
            text,
            encrypt=True
        )

    def decrypt(self, text):

        """
        Публичный метод дешифрования.
        """

        return self._process(
            text,
            encrypt=False
        )


# =========================================================
# ТЕСТ
# =========================================================

if __name__ == "__main__":

    cipher = VigenereCipher("КЛЮЧ")

    encrypted = cipher.encrypt(
        "ПРИВЕТ МИР"
    )

    decrypted = cipher.decrypt(
        encrypted
    )

    print("Encrypted:", encrypted)

    print("Decrypted:", decrypted)