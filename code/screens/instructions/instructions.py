import glob
import json

from code.modules import global_vars
from code.modules.wiimotes import *
from code.helper_functions.wrap_text import wrap_text, render_text_list


def instructions(game_number, play_music=False):
    with open("content/instructions/game_instructions.json", "r") as f:
        game_info = json.load(f)["games"][game_number]

    width, height, screen, clock, speed, character_colors, wiimotes, already_pressed = global_vars.width, global_vars.height, global_vars.screen, global_vars.clock, global_vars.speed, global_vars.character_colors, global_vars.wiimotes, global_vars.already_pressed

    title_font = pygame.font.Font('content/global/fonts/Minercraftory.ttf', height // 15)
    title_text = title_font.render(game_info["name"], True, (0, 0, 0))

    background = pygame.transform.scale(pygame.image.load("content/instructions/textures/background.png"), (width, height))

    return_button_dimension = title_font.get_height()

    width_spacing = (width // 2 - title_text.get_width() // 2 - return_button_dimension) // 2

    body_font = pygame.font.Font('content/global/fonts/Minercraftory.ttf', height // 30)
    body_surface = render_text_list(wrap_text(game_info["description"], body_font, width // 2 - (3 * width_spacing // 2)), body_font)

    height_spacing = (height - (return_button_dimension + body_surface.get_height())) // 3

    picture_width, picture_pos = ((width // 2) - (title_text.get_width() // 2)) * 4 // 5, (width // 2 + title_text.get_width() // 2 + ((width // 2) - (title_text.get_width() // 2)) // 10, height_spacing // 2)

    gameplay_width = body_surface.get_width()

    return_button = pygame.transform.scale(pygame.image.load("content/instructions/textures/back_button.png"), (return_button_dimension, return_button_dimension))
    game_picture = pygame.transform.scale(pygame.image.load(f"content/main_screen/textures/game_pictures/{game_number}.png"), (picture_width, 9 * picture_width // 16))
    gameplay_pictures = [pygame.transform.scale(pygame.image.load(i), (gameplay_width, 9 * gameplay_width // 16)) for i in glob.glob(f'content/instructions/textures/gameplay/{game_number}/*')]

    play_button_height = (height - (
                (picture_pos[1] + game_picture.get_height()) + height_spacing + gameplay_pictures[0].get_height())) // 2

    play_button = pygame.transform.scale(pygame.image.load("content/instructions/textures/play_button.png"), (play_button_height * 3//2, play_button_height))

    play_button_pos = (width * 3//4 - play_button.get_width() // 2, (picture_pos[1] + game_picture.get_height()) + height_spacing + gameplay_pictures[0].get_height() + play_button_height // 2)

    gameplay_current = 0
    selection_pointer = 0

    if play_music:
        pygame.mixer.music.load("content/instructions/sounds/background_music.mp3")
        pygame.mixer.music.play(loops=-1, fade_ms=3000)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break

        buttons = get_wiimote_button_presses(wiimotes)

        if buttons[0].count('Home') > 0:
            break

        screen.fill((255, 255, 255))

        screen.blit(background, (0, 0))

        if selection_pointer < 1:
            if buttons[0].count('Down') > 0:
                selection_pointer += 1
            elif buttons[0].count('1') > 0:
                break

        elif selection_pointer > 0:
            if buttons[0].count('Up') > 0:
                selection_pointer -= 1
            elif buttons[0].count('2') > 0:
                return True

        if buttons[0].count('B') > 0:
            break

        if selection_pointer == 0:
            pygame.draw.rect(screen, character_colors[0], pygame.Rect(width_spacing*4 // 5, height_spacing // 3, return_button_dimension + width_spacing*2 // 5, return_button_dimension + height_spacing // 3))

        elif selection_pointer == 1:
            # pygame.draw.rect(screen, character_colors[0], pygame.Rect(play_button_pos[0] - width_spacing // 4, play_button_pos[1] - height_spacing // 4, play_button_width + width_spacing * 2 // 3, play_button.get_height() + height_spacing * 2 // 3))
            pygame.draw.rect(screen, character_colors[0], pygame.Rect(play_button_pos[0] - width_spacing // 4,
                                                                      play_button_pos[1] - height_spacing // 4,
                                                                      play_button.get_width() + width_spacing // 2,
                                                                      play_button_height + height_spacing // 2))

        screen.blit(return_button, (width_spacing, height_spacing // 2))
        screen.blit(title_text, (2 * width_spacing + return_button_dimension, height_spacing // 2))
        screen.blit(game_picture, picture_pos)
        screen.blit(body_surface, (width_spacing, (height_spacing*2) + return_button_dimension))

        if gameplay_current >= len(gameplay_pictures):
            gameplay_current = 0

        screen.blit(gameplay_pictures[gameplay_current], (width // 2 + width_spacing // 2, (picture_pos[1] + game_picture.get_height()) + height_spacing))
        gameplay_current += 1

        screen.blit(play_button, play_button_pos)

        pygame.display.flip()

        clock.tick(speed)
