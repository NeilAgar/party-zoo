import pygame

from code.helper_functions.get_config import get_config
from code.modules.wiimotes import wiimote_initializer


def init(dimensions, controllers):
    pygame.init()
    pygame.mixer.init()
    pygame.display.set_caption('TITLE')

    global width, height, screen, clock, speed, user_events, total_games, total_characters, menu_lag, controller_count, character_colors, wiimotes, already_pressed, placement_colors

    controller_count = controllers
    character_colors = [(0, 0, 139), (139, 0, 0), (0, 139, 0), (230, 230, 0)]
    width, height = dimensions[0], dimensions[1]
    screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
    clock = pygame.time.Clock()
    speed = 60
    user_events = 0
    menu_lag = 0.1
    total_games = 1
    total_characters = 9
    wiimotes = wiimote_initializer()
    already_pressed = [[] for i in range(get_config()[0])]
    placement_colors = [(255, 217, 0), (192, 192, 192), (184, 115, 51), (127, 20, 145)]


def character_save(character_input):
    global character_assignment
    character_assignment = character_input
