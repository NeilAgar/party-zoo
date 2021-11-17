import time

from code.modules import global_vars
from code.modules.global_vars import character_save
from code.modules.wiimotes import *
from code.helper_functions.menu_select import get_picture_positions
from code.screens.main_screen.game_select import game_select


def character_select():
    width, height, screen, clock, speed, total_characters, menu_lag, players, character_colors, wiimotes, already_pressed = global_vars.width, global_vars.height, global_vars.screen, global_vars.clock, global_vars.speed, global_vars.total_characters, global_vars.menu_lag, global_vars.controller_count, global_vars.character_colors, global_vars.wiimotes, global_vars.already_pressed

    title_font = pygame.font.Font('content/global/fonts/Minercraftory.ttf', height//12)
    title_text = title_font.render('Choose Your Characters', True, (0, 0, 0))

    background = pygame.transform.scale(pygame.image.load("content/main_screen/textures/character_select_background.png"), (width, height))

    picture_height = 5*height//24
    picture_width = picture_height
    width_spacing = (width - 3 * picture_height) // 4
    title_height = height // 9
    button_height = height//8
    height_spacing = (height - (title_height + 3*picture_height + button_height))//6
    if width_spacing < 0:
        width_spacing = 0

    character_pictures = [pygame.transform.scale(pygame.image.load(f"content/main_screen/textures/characters/{i}.png"), (int(picture_width), int(picture_height))) for i in range(0, total_characters)]

    picture_positions = get_picture_positions(width_spacing, height_spacing,
                                              picture_width, picture_height, title_height, total_characters)

    height_spacing_count = 0
    if (total_characters % 3) > 0:
        height_spacing_count += 1
    height_spacing_count += (total_characters - (total_characters % 3)) // 3

    start_button = pygame.image.load("content/main_screen/textures/start_button.png")
    start_button = pygame.transform.scale(start_button, (start_button.get_width() * (button_height//start_button.get_height()), button_height))
    greyed_start_button = pygame.transform.scale(pygame.image.load("content/main_screen/textures/greyed_start_button.png"), (start_button.get_width(), start_button.get_height()))
    button_position = (width//2-start_button.get_width()//2, height_spacing * (height_spacing_count+2) + title_height + picture_height*height_spacing_count)

    already_pressed = [[] for i in range(get_config()[0])]

    current_characters = [[i, False] for i in range(1, players+1)]

    characters_chosen = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break

        buttons = get_wiimote_button_presses(wiimotes)

        if buttons[0].count('Home') > 0:
            break

        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play(loops=-1, fade_ms=3000)

        screen.fill((255, 255, 255))

        screen.blit(background, (0, 0))

        for player in range(players):
            current_character = current_characters[player][0]
            pygame.draw.rect(screen, character_colors[player], pygame.Rect(picture_positions[current_character-1][0]-width_spacing//4, picture_positions[current_character-1][1]-height_spacing//4, picture_width+width_spacing//2, picture_height+height_spacing//2))
            if current_characters[player][1]:
                pygame.draw.rect(screen, (112, 112, 139),
                                 pygame.Rect(picture_positions[current_character - 1][0] - width_spacing // 5,
                                             picture_positions[current_character - 1][1] - height_spacing // 8,
                                             picture_width + width_spacing*2 // 5, picture_height + height_spacing // 4))

        screen.blit(title_text, (width // 2 - title_text.get_width() // 2, 0))

        for player in range(total_characters):
            screen.blit(character_pictures[player], picture_positions[player])

        for player in range(players):
            if not current_characters[player][1]:
                if buttons[player].count('Down') > 0:
                    potential_move = current_characters[player][0] + 3
                    if potential_move <= total_characters and potential_move not in [i[0] for i in current_characters]:
                        current_characters[player][0] = potential_move
                    time.sleep(menu_lag)

                elif buttons[player].count('Up') > 0:
                    potential_move = current_characters[player][0] - 3
                    if potential_move >= 1 and potential_move not in [i[0] for i in current_characters]:
                        current_characters[player][0] = potential_move
                    time.sleep(menu_lag)

                elif buttons[player].count('Left') > 0:
                    potential_move = current_characters[player][0] - 1
                    if potential_move % 3 > 0 and potential_move not in [i[0] for i in current_characters]:
                        current_characters[player][0] = potential_move
                    time.sleep(menu_lag)

                elif buttons[player].count('Right') > 0:
                    current_pos = current_characters[player][0]
                    potential_move = current_pos + 1
                    if (current_pos - 1) % 3 < 2 and len(picture_positions) > current_pos and potential_move not in [
                        i[0] for i in current_characters]:
                        current_characters[player][0] = potential_move
                    time.sleep(menu_lag)

            if buttons[player].count('2') > 0:
                current_characters[player][1] = True
                time.sleep(menu_lag)

            elif buttons[player].count('1') > 0:
                current_characters[player][1] = False
                time.sleep(menu_lag)

        if False not in [i[1] for i in current_characters]:
            pygame.draw.rect(screen, character_colors[0], pygame.Rect(button_position[0]-start_button.get_width()//15, button_position[1]-start_button.get_height()//15, start_button.get_width()*17//15, start_button.get_height()*17//15))
            screen.blit(start_button, button_position)

            if buttons[0].count('2') > 0:
                characters_chosen = True
                character_save([i[0] for i in current_characters])
                break

        else:
            screen.blit(greyed_start_button, button_position)

        pygame.display.flip()

        clock.tick(speed)

    if characters_chosen:
        time.sleep(1)
        game_select()
