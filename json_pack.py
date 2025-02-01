from json import dump, load

def save_configure(data, fname = "data"):
    ''' Сохранение конфигурации в JSON файл. '''
    with open(f"{fname}.json", "w", encoding="utf-8") as file:
        dump(data, file)
        return True

def get_configure(fname = 'data'):
    ''' Получение конфигурации из JSON файла. '''
    try:
        with open(f"{fname}.json", "r", encoding="utf-8") as file:
            return load(file)
    except:
        return False

