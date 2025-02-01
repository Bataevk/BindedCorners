from tkinter import StringVar, Canvas,Tk
from tkinter.ttk import Style, Frame, Combobox, Button
from PIL import ImageTk, Image
from threading import Thread
from pystray import Icon, Menu, MenuItem
from os import _exit

# Подгрузка своих модулей
import get_wallpaper as gw
import json_pack as jp
import navigator as nav



# Поток для работы модуля навигации
nav_thread = None



# DATA
# Создаем изображение для значка
icon_image = Image.open("./icon.ico")

# Иннициализация окна
w_p = (10,10)
size = (600,430)
root = Tk()
root.geometry(f'{size[0]}x{size[1]}')  # Установите размер окна
root.resizable(False, False)
root.title('BindedCorners')
root.iconbitmap('./icon.ico')

# Установка стилей окна
Style().configure(".",  font=("Segoe UI", 12), foreground="#262626", background="#bdb4bf", relief='solid border') 
Style().configure("TButton",  font=("Segoe UI", 12), foreground="#262626", padding=-3) 
Style().configure("TCombobox",  font=("Segoe UI", 12), foreground="#262626", padding=3) 



# Получение сохранненой ранее конфигурации программы
corners_prompts = jp.get_configure()

# Объявление вспомогательных переменных
corner_comboxs = [None,None,None,None]


bind_labels = ('win+tab', 'win+ctrl+right','win+ctrl+left','win+a','win+r')
corners_name = ('nw','ne','sw','se')
labels = [None,None,None,None]
corner_vars = [StringVar() for _ in range(4)]




if corners_prompts:
    '''Конвертирование сохраненных комбинаций в текстовый формат. '''
    corners_prompts = corners_prompts['prompts']
    for i in range(4):
        corner_vars[i].set('+'.join(filter(lambda x: x != '', corners_prompts[i])))



# Инициализация интерфейса

window_corners = Frame(root)
window_corners.pack(fill='both', expand=True)

image_size = [0,0]
image_size[0] = (size[0] - 4*(w_p[0]))
image_size[1] = image_size[0]*9//16

image = ImageTk.PhotoImage(Image.open(gw.wallpaper_path).resize(image_size))
canv = Canvas(window_corners, width=image_size[0]+w_p[0], height=image_size[1]+w_p[1], bg='black')
canv.place(x=size[0]//2, y=size[1]//2, anchor='center')
canv.create_image(w_p[0]*0.7,w_p[1]*0.7, image=image, anchor = "nw")

for i in range(len(corner_vars)):
    corner_comboxs[i] = Combobox(window_corners,textvariable=corner_vars[i])
    corner_comboxs[i]['values'] = bind_labels
    corner_comboxs[i].place(x=i%2*(size[0]) + w_p[0]*(1-i%2*2), y=w_p[1]*(1-(i//2)*2) + (size[1])*(i//2), anchor = corners_name[i])



# Functions

def on_close():
    ''' Скрытие окна. '''
    root.withdraw()

def nav_start():
    ''' Запуск модуля навигации. '''
    nav_thread = Thread(target=nav.run)
    nav.Prompts = corners_prompts
    nav_thread.start()

def nav_pause():
    if nav.running:
        main_button['text'] = 'RUN'
        nav.stop()
        return
    
    nav_start()
    main_button['text'] = 'STOP'

def func_button():
    ''' Обработка нажатия кнопки "RUN" и "STOP".'''
    global corners_prompts
    corners_prompts = []

    for var_c in corner_vars:
        corners_prompts.append(nav.text_to_prompt(var_c.get()))

    jp.save_configure({'prompts':corners_prompts})
    
    nav_pause()
    


# Созднаие главного кнопки
main_button = Button(window_corners, text="RUN", command=func_button)
main_button.place(x=size[0]//2, y=size[1] - w_p[1], anchor='s')

# Переназначение функции кнопки "крестик"
root.protocol("WM_DELETE_WINDOW", on_close)

# Создание иконки на панели задач Windows
icon = Icon("BindedCorners", icon_image, "BindedCorners",  menu=Menu(MenuItem("Open", root.deiconify), MenuItem("Run/Stop", nav_pause), MenuItem("Close", root.destroy)))
icon_thread = Thread(target=icon.run)
icon_thread.start()


# Запуск окна
if __name__ == '__main__':
    root.mainloop()
    icon.stop()
    nav.stop()

    _exit(0)