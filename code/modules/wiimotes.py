import pygame

from code.helper_functions.get_config import get_config


def wiimote_initializer():
    pygame.init()

    try:
        wiimotes = [pygame.joystick.Joystick(j) for j in range(get_config()[0])]
    except pygame.error:
        print("Wiimotes are not connected.")
        return False

    return wiimotes


def get_wiimote_button_presses(wiimotes):
    for wiimote in wiimotes:
        wiimote.init()

    buttons = []

    for wiimote in wiimotes:
        current_buttons = []

        if wiimote.get_button(0):
            current_buttons.append("Down")
        if wiimote.get_button(1):
            current_buttons.append("Up")
        if wiimote.get_button(2):
            current_buttons.append("Left")
        if wiimote.get_button(3):
            current_buttons.append("Right")
        if wiimote.get_button(4):
            current_buttons.append("A")
        if wiimote.get_button(5):
            current_buttons.append("B")
        if wiimote.get_button(6):
            current_buttons.append("+")
        if wiimote.get_button(7):
            current_buttons.append("-")
        if wiimote.get_button(8):
            current_buttons.append("Home")
        if wiimote.get_button(9):
            current_buttons.append("1")
        if wiimote.get_button(10):
            current_buttons.append("2")

        buttons.append(current_buttons)

    return buttons


def get_individual_buttons(raw_input, already_pressed):
    output = [[] for i in range(get_config()[0])]

    for player in range(len(already_pressed)):
        already_pressed_temp = list(already_pressed[player])
        for button in already_pressed[player]:
            if button not in raw_input:
                already_pressed_temp.remove(button)

        already_pressed[player] = already_pressed_temp

    for player in range(len(raw_input)):
        for button in raw_input[player]:
            if button not in already_pressed[player]:
                output[player].append(button)
                already_pressed[player].append(button)

    return output
