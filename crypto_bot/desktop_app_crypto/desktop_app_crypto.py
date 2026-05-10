from tkinter import ttk
import tkinter as tk
# messagebox — готовые всплывающие окна (ошибки, уведомления)
from tkinter import messagebox, filedialog

# Импорт нашей бизнес-логики (шифр Цезаря)
# Важно: UI ничего не знает о реализации — только вызывает методы
from crypto_bot.src.caesar import Caesar

class CaesarApp:
    def __init__(self, root):
        # root — это главное окно приложения (его создаём ниже)
        self.root = root

        # Устанавливаем заголовок окна
        self.root.title("Caesar Cipher")

        # ---------------- UI СОЗДАЁТСЯ СВЕРХУ ВНИЗ ---------------- #
        tk.Button(root, text="Загрузить текст из файла", command=self.copy_file).pack(pady=5)
        # 1. Надпись "Введите текст"
        # Когда ты создаёшь элемент, он ещё не отображается
        # Чтобы он появился — нужно сказать: "положи его в окно"
        # И вот это делает: .pack()
        tk.Label(root, text="Введите текст:").pack()

        # Поле для ввода текста (многострочное)
        self.input_text = tk.Text(root, height=5, width=40)
        self.input_text.pack()

        # 2. Надпись "Сдвиг"
        tk.Label(root, text="Сдвиг:").pack()
        # StringVar —
        # специальная tkinter-переменная
        # для хранения состояния UI

        self.cipher_var = tk.StringVar()

        # Значение по умолчанию
        self.cipher_var.set("Caesar")

        # Combobox = dropdown список

        self.cipher_dropdown = ttk.Combobox(
            root,

            textvariable=self.cipher_var,

            values=[
                "Caesar",
                "Vigenere"
            ],

            state="readonly"
        )

        self.cipher_dropdown.pack(pady=5)
        # Поле ввода (однострочное) для числа (shift)
        self.shift_entry = tk.Entry(root)
        self.shift_entry.pack()

        # 3. КНОПКИ
        # command=self.encrypt — при нажатии вызывается метод encrypt()
        # .pack(pady=5) - размести элемент и добавь вертикальные отступы по 5 пикселей сверху и снизу
        tk.Button(root, text="Encrypt", command=self.encrypt).pack(pady=5)
        tk.Button(root, text="Decrypt", command=self.decrypt).pack(pady=5)

        # 4. Поле результата
        tk.Label(root, text="Результат:").pack()

        self.output_text = tk.Text(root, height=5, width=40)
        self.output_text.pack()
        tk.Button(root, text="Сохранить результат в файл результата", command=self.append_result_file).pack(pady=5)

        # 5. Кнопка скопировать
        tk.Button(root, text="Copy", command=self.copy_result).pack(pady=5)
    # ---------------- ВСПОМОГАТЕЛЬНАЯ ЛОГИКА ---------------- #
    def copy_file(self):
        file_path = filedialog.askopenfilename(title="Выберите файл", filetypes=[('text file', '*.txt'), ('all files', '.*')])
        with open(file_path, 'r', encoding= 'utf-8') as filef:
            data = filef.read()
            self.input_text.delete("1.0", tk.END)
            self.input_text.insert(tk.END, data)

    def append_result_file(self):
        with open('result.txt', 'w', encoding= 'utf-8') as filef:
            data = filef.write(self.output_text.get('1.0', tk.END))

    def copy_result(self):
        # Получаем текст из поля результата
        text = self.output_text.get("1.0", tk.END).strip()

        if not text:
            messagebox.showinfo("Info", "Нечего копировать")
            return

        # Очищаем буфер обмена
        self.root.clipboard_clear()

        # Копируем текст
        self.root.clipboard_append(text)

        # Обновляем буфер (важно для некоторых систем)
        self.root.update()

        messagebox.showinfo("Успех", "Текст скопирован!")

    def get_cipher(self):
        """
        Этот метод:
        1. Берёт значение shift из UI
        2. Проверяет, что это число
        3. Создаёт объект CaesarCipher
        """

        try:
            # Получаем текст из поля ввода и превращаем в int
            shift = int(self.shift_entry.get())

            # Создаём объект шифра
            return Caesar(shift)

        except ValueError:
            # Если пользователь ввёл не число → показываем ошибку
            messagebox.showerror("Ошибка", "Сдвиг должен быть числом")

            # Возвращаем None → сигнал, что дальше работать нельзя
            return None

    # ---------------- ЛОГИКА КНОПКИ ENCRYPT ---------------- #

    def encrypt(self):
        """
        Последовательность работы:
        1. Получаем объект шифра
        2. Берём текст из UI
        3. Шифруем
        4. Выводим результат
        """

        # 1. Получаем шифр
        cipher = self.get_cipher() # CaesarCipher(shift)

        # Если ошибка (None) — останавливаем выполнение
        if not cipher:
            return

        # 2. Получаем текст из Text widget
        # "1.0" — начало текста (строка 1, символ 0)
        # tk.END — конец текста
        text = self.input_text.get("1.0", tk.END).strip()

        try:
            # 3. Шифруем текст
            result = cipher.encrypt(text)

            # 4. Очищаем поле результата
            self.output_text.delete("1.0", tk.END)

            # Вставляем новый результат
            self.output_text.insert(tk.END, result)

        except Exception as e:
            # Если ошибка в логике шифрования — показываем её
            messagebox.showerror("Ошибка", str(e))

    # ---------------- ЛОГИКА КНОПКИ DECRYPT ---------------- #

    def decrypt(self):
        """
        Логика почти такая же как encrypt:
        отличие только в методе decrypt()
        """

        cipher = self.get_cipher()

        if not cipher:
            return

        text = self.input_text.get("1.0", tk.END).strip()

        try:
            result = cipher.decrypt(text)

            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, result)

        except Exception as e:
            messagebox.showerror("Ошибка", str(e))


# ---------------- ТОЧКА ВХОДА ---------------- #

if __name__ == "__main__":
    """
    Это старт приложения:

    1. Создаём главное окно
    2. Передаём его в наш класс (инициализация UI)
    3. Запускаем бесконечный цикл обработки событий
    """

    # Создание окна
    root = tk.Tk()

    # Создание приложения (отрисовывает UI)
    app = CaesarApp(root)

    # Запуск цикла событий (клики, ввод и т.д.)
    root.mainloop()