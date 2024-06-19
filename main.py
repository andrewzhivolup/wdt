import math
import os
import random
import sys
import time

import cv2
import keyboard
import mss
import numpy as np
import pygetwindow as gw
import win32api
import win32con


# получаем файлы изображения если приложение открыто через .exe
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
        return str(os.path.join(base_path, relative_path))
    except Exception:
        return relative_path

class AutoClicker:
    def __init__(self, window_title, max_clicks, windows_count):
        self.window_title = window_title
        self.running = False
        self.clicked_points = []
        self.iteration_count = 0
        self.max_clicks = max_clicks
        self.windows_count = windows_count
        self.max_clicks_for_all_windows = int(max_clicks) * int(windows_count)

        self.templates_plays = [
            cv2.cvtColor(cv2.imread(img, cv2.IMREAD_UNCHANGED), cv2.COLOR_BGRA2GRAY) for img in CLICK_IMAGES
        ]  # картинки по которым нужно кликать

    @staticmethod
    def click_at(x, y):
        random_x_1 = random.randint(25, 55)
        random_x_2 = random.randint(25, 55)
        random_y_1 = random.randint(25, 55)
        random_y_2 = random.randint(25, 55)
        _x = x + int(random_x_1) - int(random_x_2)
        _y = y + int(random_y_1) - int(random_y_2)

        win32api.SetCursorPos((_x, _y))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, _x, _y, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, _x, _y, 0, 0)

    def toggle_script(self):
        self.running = not self.running
        r_text = "вкл" if self.running else "выкл"
        print(f'Статус изменен: {r_text}')

    def find_and_click_image(self, template_gray, screen, monitor):

        screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGRA2GRAY)

        result = cv2.matchTemplate(screen_gray, template_gray, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        if max_val >= 0.6:
            template_height, template_width = template_gray.shape
            center_x = max_loc[0] + template_width // 2 + monitor["left"]
            center_y = max_loc[1] + template_height // 2 + monitor["top"]
            self.click_at(center_x, center_y)
            return True

        return False

    def start(self):
        windows = gw.getWindowsWithTitle(self.window_title)

        if not windows:
            print(f"Не найдено окна с заголовком: {self.window_title}.")
            return

        window = windows[0]
        window.activate()


        with mss.mss() as sct:
            grave_key_code = 41
            keyboard.add_hotkey(grave_key_code, self.toggle_script)

            while True:
                if self.running:
                    monitor = {
                        "top": window.top,
                        "left": window.left,
                        "width": window.width,
                        "height": window.height
                    }
                    img = np.array(sct.grab(monitor))

                    random_float = random.uniform(0.4, 0.6)

                    time.sleep(random_float)
                    for tp in self.templates_plays:
                        self.find_and_click_image(tp, img, monitor)


if __name__ == "__main__":
    CLICK_IMAGES = [resource_path("media\\wepc1.png")]

    # ограничение кликов
    # answer = None
    # while answer is None:
    #     answer = input("Укажите максимальное количество кликов (по-умолчнию: 70000): ")
    #     if answer.isdigit() == False:
    #         answer = 70000
    max_clicks = 70000

    # ограничение окон 
    # answer = None
    # while answer is None:
    #     answer = input("Укажите максимальное количество окон (по-умолчнию: 1): ")
    #     if answer.isdigit() == False:
    #         answer = 1
    windows_count = 1

    print('Для запуска скрипта нажми "ё" (`) на клавиатуре')

    auto_clicker = AutoClicker("LDPlayer", max_clicks, windows_count)
    try:
        auto_clicker.start()
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    for i in reversed(range(5)):
        i += 1
        print(f"Скрипт завершит работу через {i}")
        time.sleep(1)
