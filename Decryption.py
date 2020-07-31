# импортируем нужные библиотеки
from time import time, sleep
from tkinter import *
from PIL import ImageTk, Image
import difflib
from math import ceil

# отображаемое на экране изображение
img = ''
current_image = ''

# номер сцены
scene_number = 0

# время начала\конца уровня
start_time = 0
end_time = 0

# считываем файл с сообщениями
messages = []

texts = open('message(s).txt')
for line in texts:
    messages.append(line)
# главное окно
root = Tk()
root.title('Decryption')
root.resizable(0, 0)
root.geometry('960x540')
root['bg'] = 'black'
# поле для графических элементов
canvas = Canvas(root, bg='pink')

# поле вывода сообщений и статичных изображений
message = Label(root, width=960, height=540, bg='black', fg="white", wraplength=250, font='20', text=messages[0])
message.pack()


# функция смены сцены
def next_scene(event):
    global scene_number, current_image, img
    scene_number += 1
    message.pack_forget()
    # первая сцена
    if scene_number == 1:
        # запоминаем время начала уровня
        start_time = ceil(time())
        # изменяем главное окно под картинку
        root.geometry('491x504')
        # изменяем отображаемую картинку в поле вывода
        img = Image.open('images/1.jpg')
        current_image = ImageTk.PhotoImage(img)
        message.config(width=491, height=680, image=current_image)
        message.pack()
        # окно для ввода текста для 1ой сцены
        input_window = Toplevel()
        input_window.geometry('245x340')
        input_window.resizable(0, 0)
        input_window.title('Text input field')
        # поле ввода текста для 1ой сцены
        input_text = Text(input_window, width=245, height=18, font='20', wrap=WORD)
        input_text.pack(expand=False)

        # функция проверки текста на правильность

        def correctness_check():
            global end_time
            # запоминаем время конца
            end_time = ceil(time())
            # считаем время прохождения
            total_time = str((end_time - start_time) // 60) + ' мин ' + str((end_time - start_time) % 60) + ' сек'
            # считываем правильный текст и убираем пробелы и запятые
            right_text = open('Decrypted_text.txt').read().replace(',', '').lower().split()
            # считываем введенный текст, убираем пробелы, запятые, заменяем ё на е
            text = input_text.get('1.0', END).lower().replace(',', '').replace('ё', 'е').split()
            # расчитываем рейтинг
            s = difflib.SequenceMatcher(lambda x: x == " ", right_text, text)
            rate = round(s.ratio(), 2)
            print(rate)
            if rate == 1.0:
                input_window.destroy()
                message.config(image='',
                               text='Поздравляем, вы расшифровали письмо абслоютно верно! Вы справились за ' + str(
                                   total_time))
            else:
                input_window.destroy()
                message.config(image='',
                               text='Вы справились за ' + str(
                                   total_time) + ' рейтинг схожести текста ' + str(int(
                                   rate * 100)) + '/100')

        # кнопка для отправки текста на проверку правильности
        send_button = Button(input_window, text="Отправить", command=correctness_check)
        send_button.pack(side=BOTTOM)
    elif scene_number == 2:
        message.config(text='Конец игры')
        message.pack()
    elif scene_number == 3:
        root.quit()


root.bind('<Button-1>', next_scene)

root.mainloop()
