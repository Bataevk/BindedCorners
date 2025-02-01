import ctypes

SPI_GETDESKWALLPAPER = 0x0073 # Код для получения пути для обоев.
MAX_PATH = 260 # Максимальное количество пути для обоев.

wallpaper_path = ctypes.create_unicode_buffer(MAX_PATH) # Создание буфера для пути для обоев.

# Вызов функции SystemParametersInfoW для получения пути обоев
ctypes.windll.user32.SystemParametersInfoW(SPI_GETDESKWALLPAPER, MAX_PATH, wallpaper_path, 0)
wallpaper_path = str(wallpaper_path.value) # Преобразование буфера в строку.
