import tkinter
from tkinter import messagebox 
#from crypto_bot.src.caesar import Caesar

class CaesarApp:
    def __init__(self, root):
        self.root = root 
        self.root.title('CryptoApp')
        tkinter.Label(root, text = 'Введите текст:').pack()
        self.input_text = tkinter.Text(root, width = 60, height = 5).pack(pady = 5)
        tkinter.Label(root, text = 'Введите сдвиг:').pack()
        self.shift_entry = tkinter.Entry(root).pack()
        tkinter.Button(root, text = 'Encrypt', command = self.test).pack()
    
    def test(self):
        pass

if __name__ == '__main__':
    root = tkinter.Tk()
    app = CaesarApp(root)
    root.mainloop()