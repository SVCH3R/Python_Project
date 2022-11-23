import os
import PySimpleGUI as sg
from vernamcipher.cryptographic import Cryptographic


# шифр Виженера
def Vigenere():
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
                (ord(plain[i]) + (ord(longkey[i])
                 if not reverse else -ord(longkey[i])))
                % 256
            )
        )
    file.close()


# шифр Вернама
def Vernam():
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
def Ceasar():
    global path, key, reverse
    file = open(path, "r")
    new_file = open("ciph.txt", "w")
    for i in file.readlines():
        for j in i:
            new_file.write(
                chr(ord(j) + (int(key) if not reverse else (-int(key)))))
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
def Cypher_Window():
    global choise, key, path
    sg.theme("DarkTeal11")
    layout = [
        [sg.Text("путь к исходному файлу"), sg.InputText(), sg.FileBrowse()],
        [sg.Text("введите ключ"), sg.Input(key="key")],
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


def Hack_Window():
    global path
    sg.theme("DarkTeal11")
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


def Output_Hack():
    sg.theme("DarkTeal11")
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


def Hack():
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
    Ceasar()


# прощальное окно


def Output_Window():
    sg.theme("DarkTeal11")
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


# стартовое окно выбоа
def firstwindow():
    global choise, reverse
    sg.theme("DarkTeal11")
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


reverse = False
choise = ""
key = ""
path = ""

# проверка на путой ввод
while choise not in [
    "шифр Цезаря",
    "шифр Виженера",
    "шифр Вернама",
    "взлом шифра Цезаря",
    -1,
]:
    firstwindow()


if choise != "взлом шифра Цезаря":
    Cypher_Window()
    if choise == "шифр Цезаря":
        Ceasar()
        Output_Window()
    if choise == "шифр Виженера":
        Vigenere()
        Output_Window()
    if choise == "шифр Вернама":
        Vernam()
        Output_Window()
else:
    Hack_Window()
    Hack()
    Output_Hack()
