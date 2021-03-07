import cv2
import os
import time
import numpy as np
from PIL import ImageGrab
from pynput.keyboard import Key, Controller as KeyboardController
from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Listener

keyboard = KeyboardController()
mouse = MouseController()

mouse = MouseController()
keyboard = KeyboardController()

os.system("Start /max mspaint")
time.sleep(1)
START_POS = (200, 200)
mouse.position = START_POS


def on_press(key):
    if key == Key.esc:
        os._exit(1)


def find_edit_button():
    edit_colors_button = cv2.imread("Templates/edit_colors_button.png")
    h, w, c = edit_colors_button.shape
    img = ImageGrab.grab(bbox=None)
    img = np.array(img)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    res = cv2.matchTemplate(img, edit_colors_button, cv2.TM_SQDIFF)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    top_left = min_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    center = ((top_left[0] + bottom_right[0]) / 2, (top_left[1] + bottom_right[1]) / 2)
    return center


def find_fields():
    field = cv2.imread("Templates/color_field.png")
    ok_button = cv2.imread("Templates/ok_button.png")
    h, w, c = field.shape
    img = ImageGrab.grab(bbox=None)
    img = np.array(img)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    res = cv2.matchTemplate(img, field, cv2.TM_SQDIFF)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    top_left = min_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    red = ((top_left[0] + bottom_right[0]) / 2, (top_left[1] + bottom_right[1]) / 2)
    blue = (red[0], red[1] + 20)
    green = (red[0], red[1] + 40)
    res = cv2.matchTemplate(img, ok_button, cv2.TM_SQDIFF)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    top_left = min_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    button = ((top_left[0] + bottom_right[0]) / 2, (top_left[1] + bottom_right[1]) / 2)

    ret = {
        "red": red,
        "blue": blue,
        "green": green,
        "ok": button
    }
    return ret


def clear_field():
    for i in range(3):
        time.sleep(0.05)
        keyboard.press(Key.backspace)
        time.sleep(0.05)
        keyboard.press(Key.delete)


def update_RGB(grayThresh):
    mouse.position = find_edit_button()
    mouse.click(Button.left, 1)
    time.sleep(0.5)
    fields = find_fields()
    mouse.position = fields["red"]
    mouse.click(Button.left, 1)
    clear_field()
    keyboard.type(str(grayThresh))
    mouse.position = fields["blue"]
    mouse.click(Button.left, 1)
    clear_field()
    keyboard.type(str(grayThresh))
    mouse.position = fields["green"]
    mouse.click(Button.left, 1)
    clear_field()
    keyboard.type(str(grayThresh))

    time.sleep(0.1)
    mouse.position = fields["ok"]
    mouse.click(Button.left, 1)
    mouse.position = START_POS
    time.sleep(0.1)


def draw_image(imgPath):
    img = cv2.imread(imgPath)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    grayThresh = 0
    threshStep = 1

    while grayThresh < 255:
        print("GrayThresh :", grayThresh)
        print(str(int((grayThresh / 255) * 100)) + "%")
        if grayThresh in img:
            print("GrayThresh: " + str(grayThresh))
            update_RGB(grayThresh)
        else:
            grayThresh += threshStep
            continue

        for i in range(len(img)):
            mouse.position = (START_POS[0], mouse.position[1])
            mouse.move(0, 1)
            for j in range(len(img[i])):
                if grayThresh - threshStep < img[i, j, 0] and img[i, j, 0] <= grayThresh:
                    mouse.click(Button.left, 1)
                    time.sleep(0.0005)
                mouse.move(1, 0)
        grayThresh += threshStep


listener = Listener(on_press=on_press)
listener.start()
draw_image("Images/biasalah.png")
