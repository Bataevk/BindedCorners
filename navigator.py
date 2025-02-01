import pyautogui as ptg
from time import sleep

# Отключение экстренного выхода при наведении курсора мыши в левый верхний угол
ptg.FAILSAFE = False 

running = False # Переменная, отображающая состояние модуля
Prompts = [] # Список комбинаций клавиш в формате, который принимает функция hotkey


# Отслеживание курсора мыши в разных углах

def is_bottom_left():
    return ptg.position()[0] == 0 and ptg.position()[1] == (ptg.size()[1] -1)

def is_bottom_right():
    return ptg.position()[0] == (ptg.size()[0]-1) and (ptg.position()[1] == ptg.size()[1]-1)

def is_top_left():
    return ptg.position()[0] == 0 and ptg.position()[1] == 0

def is_top_right():
    return ptg.position()[0] == (ptg.size()[0]-1) and ptg.position()[1] == 0

def text_to_prompt(text: str):
    ''' Преобразование текста в список комбинаций в необходимом формате. '''
    promt = text.split('+')
    promt.extend([''] * (4 - len(promt)))
    return promt

def navigate(promt):
    ''' Иммитация клавиш с обработкой ошибок'''
    try:
        ptg.hotkey(promt)
        return True
    except Exception as e:
        print(e)
        return False
    


def switch_pause(value: bool = not running):
    ''' Переключение состояния модуля. '''
    global running
    running = value

def stop():
    ''' Остановка модуля. '''
    switch_pause(False)


def get_index():
    ''' Получение индекса угла. '''
    if is_top_left(): return 0
    if is_top_right(): return 1
    if is_bottom_left(): return 2
    if is_bottom_right(): return 3
    return -1
        
def run():
    ''' Запуск модуля. '''
    switch_pause(True)

    # Прошлый индекс, нужен для избежания повторного срабатывания
    prev_index = -1

    while running:
        ''' Главный цикл, который отслуживает мышь и осуществляет иммитацию нажатия клавиш. '''
        index = get_index()
        if prev_index != index:
            prev_index = index
            if (index > -1 and index < 4):
                navigate(Prompts[index])
        sleep(0.01)