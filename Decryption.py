# импортируем нужные библиотеки
from tkinter import *
from PIL import ImageTk, Image
from time import time
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
        root.geometry('491x680')
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
            total_time = str((end_time-start_time) // 60) + ' мин ' + str((end_time-start_time) % 60) + ' сек'
            # считываем правильный текст
            right_text = open('Decrypted_text.txt')
            right_text = right_text.read()
            # убираем пробелы и запятые
            right_text = right_text.replace(',', '')
            right_text = right_text.replace(' ', '')
            # считываем введенный текст
            text = input_text.get('1.0', END)
            # убираем пробелы и запятые
            text = text.replace(',', '')
            text = text.replace(' ', '')
            mistakes = 0
            for i in range(len(right_text)):
                try:
                    if text[i] != right_text[i]:
                        mistakes += 1
                except:
                    mistakes += 1
            print(mistakes)
            if mistakes == 0:
                input_window.destroy()
                message.config(image='',
                               text='Поздравляем, вы расшифровали письмо абслоютно верно! Вы справились за ' + str(
                                   total_time))
            else:
                input_window.destroy()
                message.config(image='',
                               text='Поздравляем, вы справились за ' + str(
                                   total_time) + ' количество ваших ошибок ' + str(
                                   mistakes))

        # кнопка для отправки текста на проверку правильности
        send_button = Button(input_window, text="Отправить", command=correctness_check)
        send_button.pack(side=BOTTOM)


root.bind('<Button-1>', next_scene)

root.mainloop()

