import os
import PySimpleGUI as sg
from vernamcipher.cryptographic import Cryptographic


class CipherApp():
    # шифр Виженера
    def Vigenere(self):
        global path, key, reverse
        file = open(path, "r")
        plain = ""
        for i in file.readlines():
            plain += i
        file.close()
        file = open(path, "w")
        length = len(plain)

        longkey = ""
        for i in range(length):
            longkey += key[i % len(key)]
        for i in range(length):
            file.write(
                chr(
                    (ord(plain[i]) + (ord(longkey[i]) if not reverse else -ord(longkey[i]))) % 255)
            )
        file.close()

    # шифр Вернама

    def Vernam(self):
        global path, key, reverse
        result = ""
        file = open(path, "r")
        plain = ""
        for i in file.readlines():
            plain += i
        length = len(plain)
        longkey = ""
        for i in range(length):
            longkey += key[i % len(key)]
        encrypted = Cryptographic.exclusive_operations(plain, longkey)
        file.close()
        file = open(path, "w")
        file.write(encrypted)
        file.close()

    # шифр Цезаря

    def Ceasar(self):
        global path, key, reverse
        file = open(path, "r")
        new_file = open("ciph.txt", "w")
        for i in file.readlines():
            for j in i:
                new_file.write(
                    chr((ord(j) + (int(key) if not reverse else (-int(key)))) % 255))
        new_file.close()
        file.close()
        new_file = open("ciph.txt", "r")
        file = open(path, "w")
        for i in new_file.readlines():
            for j in i:
                file.write(j)

        new_file.close()
        file.close()
        os.remove("ciph.txt")

    # ввод ключа и пути к файлу, который нужно зашифровать

    def Cypher_Window(self):
        global choise, key, path
        sg.theme("DarkTeal5")
        layout = [
            [sg.Text("путь к исходному файлу"),
             sg.InputText(), sg.FileBrowse()],
            [sg.Text("введите ключ*"), sg.Input(key="key")],
            [sg.Text("*ключ для шифра Цезаря - число или символ, Виженера и Вернама - строка")],
            [sg.Button("OK")],
        ]
        window = sg.Window(choise, layout)
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED:
                exit(0)
            if event == "OK":
                key = values["key"]
                path = values["Browse"]
                break

        window.close()
        return 0

    def Hack_Window(self):
        global path
        sg.theme("DarkTeal5")
        layout = [[sg.Text("путь к файлу"), sg.InputText(), sg.FileBrowse()],
                  [sg.Button("OK")]]
        window = sg.Window(choise, layout)
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED:
                exit(0)
            if event == "OK":
                path = values[0]
                break
        window.close()
        return 0

    def Output_Hack(self):
        sg.theme("DarkTeal5")
        layout = [[sg.Text("произведена попытка взлома")], [sg.Button("OK")]]
        window = sg.Window("", layout)
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED:
                break
            if event == "OK":
                break

        window.close()
        return 0

    def Hack(self):
        global path, key
        file = open(path, "r")
        plain = ""
        for i in file.readlines():
            plain += i.lower()
        length = len(plain)
        freqset = list(set(plain))
        freqdict = {i: plain.count(i) for i in freqset}
        freqdict[' '] = 0
        freqdict = {plain.count(i): i for i in freqset}
        freqs = sorted(freqdict.keys())
        max_freq = freqdict[freqs[0]]
        print(freqdict)
        key = ord(" ") - ord(max_freq)
        reverse = True
        self.Ceasar()

    # прощальное окно

    def Output_Window(self):
        sg.theme("DarkTeal5")
        layout = [[sg.Text("файл изменен")], [sg.Button("OK")]]
        window = sg.Window("", layout)
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED:
                break
            if event == "OK":
                break

        window.close()
        return 0

    # стартовое окно выбора

    def firstwindow(self):
        global choise, reverse
        sg.theme("DarkTeal5")
        layout = [
            [sg.Text("выберите тип операции:")],
            [sg.Checkbox("расшифровать")],
            [
                sg.Combo(
                    ["шифр Цезаря", "шифр Виженера",
                        "шифр Вернама", "взлом шифра Цезаря"]
                )
            ],
            [sg.Button("OK")],
        ]
        window = sg.Window("", layout)
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED:
                choise = -1
                exit(0)
            if event == "OK":
                choise = values[1]
                reverse = values[0]
                break
        window.close()

    def start(self):
        global choise, reverse
        choise = ""
        # проверка на путой ввод
        while choise not in [
            "шифр Цезаря",
            "шифр Виженера",
            "шифр Вернама",
            "взлом шифра Цезаря",
            -1,
        ]:
            self.firstwindow()

        if choise != "взлом шифра Цезаря":
            self.Cypher_Window()
            if choise == "шифр Цезаря":
                self.Ceasar()
                self.Output_Window()
            if choise == "шифр Виженера":
                self.Vigenere()
                self.Output_Window()
            if choise == "шифр Вернама":
                self.Vernam()
                self.Output_Window()
        else:
            self.Hack_Window()
            self.Hack()
            self.Output_Hack()


def main():

    app = CipherApp()
    app.start()


if __name__ == '__main__':
    main()
