import time

from code.modules import global_vars
from code.modules.wiimotes import *
from code.helper_functions.menu_select import get_picture_positions
from code.screens.game_intro.game_intro import game_intro
from code.screens.instructions.instructions import instructions
from code.screens.end_screen.end_screen import end_screen


def game_select():
    width, height, screen, clock, speed, total_games, menu_lag, character_colors, wiimotes, already_pressed = global_vars.width, global_vars.height, global_vars.screen, global_vars.clock, global_vars.speed, global_vars.total_games, global_vars.menu_lag, global_vars.character_colors, global_vars.wiimotes, global_vars.already_pressed

    title_font = pygame.font.Font('content/global/fonts/Minercraftory.ttf', height//9)
    title_text = title_font.render('Choose A Game', True, (0, 0, 0))

    background = pygame.transform.scale(pygame.image.load("content/main_screen/textures/game_select_background.png"), (width, height))

    width_spacing = width / 20
    picture_width = width * 4 / 15
    picture_height = width * 3 / 20
    title_height = height / 9
    height_spacing = (height - title_height - 3 * picture_height) / 5
    if height_spacing < 0:
        height_spacing = 0

    game_pictures = [pygame.transform.scale(pygame.image.load(f"content/main_screen/textures/game_pictures/{i}.png"), (int(picture_width), int(picture_height))) for i in range(0, total_games)]

    picture_positions = get_picture_positions(width_spacing, height_spacing,
                                              picture_width, picture_height, title_height, total_games)

    current_game = 1

    game_chosen = False
    music_played = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break

        buttons = get_wiimote_button_presses(wiimotes)

        if buttons[0].count('Home') > 0:
            break

        screen.fill((255, 255, 255))

        screen.blit(background, (0, 0))

        pygame.draw.rect(screen, character_colors[0], pygame.Rect(picture_positions[current_game-1][0]-width_spacing//2, picture_positions[current_game-1][1]-height_spacing//2, picture_width+width_spacing, picture_height+height_spacing))

        screen.blit(title_text, (width / 2 - title_text.get_width() / 2, 0))

        for num in range(total_games):
            screen.blit(game_pictures[num], picture_positions[num])

        if buttons[0].count('2') > 0:
            time.sleep(1)
            if not music_played:
                music_played = True
                if instructions(current_game - 1, play_music=True):
                    music_played = False
                    game_results = game_intro(current_game - 1)
                    if game_results:
                        while True:
                            if game_results:
                                if end_screen(game_results):
                                    game_results = game_intro(current_game - 1)
                                else:
                                    time.sleep(1)
                                    break

            else:
                if instructions(current_game - 1):
                    music_played = False
                    game_results = game_intro(current_game - 1)
                    if game_results:
                        while True:
                            if game_results:
                                if end_screen(game_results):
                                    game_results = game_intro(current_game - 1)
                                else:
                                    time.sleep(1)
                                    break

        elif buttons[0].count('Down') > 0:
            current_game += (3 if current_game + 3 <= total_games else 0)
            time.sleep(menu_lag)

        elif buttons[0].count('Up') > 0:
            current_game -= (3 if current_game - 3 >= 1 else 0)
            time.sleep(menu_lag)

        elif buttons[0].count('Left') > 0:
            current_game -= (1 if (current_game - 1) % 3 > 0 else 0)
            time.sleep(menu_lag)

        elif buttons[0].count('Right') > 0:
            current_game += (1 if (current_game - 1) % 3 < 2 and len(picture_positions) > current_game else 0)
            time.sleep(menu_lag)

        pygame.display.flip()

        clock.tick(speed)
