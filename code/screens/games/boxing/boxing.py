import time

from code.modules import global_vars
from code.modules.wiimotes import *
import code.modules.global_vars


def boxing():
    width, height, screen, clock, speed, character_colors, wiimotes, already_pressed, controller_count, user_events = global_vars.width, global_vars.height, global_vars.screen, global_vars.clock, global_vars.speed, global_vars.character_colors, global_vars.wiimotes, global_vars.already_pressed, global_vars.controller_count, global_vars.user_events

    wiimotes = wiimote_initializer()

    punch_sound = pygame.mixer.Sound("content/games/0/sounds/punch.mp3")
    punch_sound.set_volume(0.1)
    whistle_start_sound = pygame.mixer.Sound("content/games/0/sounds/whistle_start.mp3")
    whistle_end_sound = pygame.mixer.Sound("content/games/0/sounds/end_game.mp3")
    pygame.mixer.music.load("content/games/0/sounds/background_music.mp3")

    background = pygame.transform.scale(pygame.image.load("content/games/0/background.jpeg"),
                                        (width, height))
    gloves = [pygame.image.load(f"content/games/0/gloves/{i}.png") for i in range(4)]
    punching_bag = pygame.image.load("content/games/0/punching_bag.png")
    border_positions = [(((i * width) // controller_count, 0), ((i * width) // controller_count, height)) for i in range(controller_count)]

    selection_width = width // controller_count

    glove_width = selection_width * 2 // 5
    glove_height = (gloves[0].get_height() * glove_width) // gloves[0].get_width()
    gloves = [pygame.transform.scale(i, (glove_width, glove_height)) for i in gloves]

    punching_bag_height = 4 * (height - glove_height) // 5
    punching_bag_width = (punching_bag.get_width() * punching_bag_height) // punching_bag.get_height()
    punching_bag = pygame.transform.scale(punching_bag, (punching_bag_width, punching_bag_height))

    hand_location = [None for i in range(controller_count)]

    # Opening Sequence

    screen.fill((255, 255, 255))
    screen.blit(background, (0, 0))
    screen.blit(punching_bag, (width // 2 - (punching_bag.get_width() // 2), 0))

    pygame.display.flip()
    clock.tick(speed)

    global_vars.user_events += 1
    pygame.time.set_timer(pygame.USEREVENT + user_events, 1000)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT + user_events:
                running = False

    global_vars.user_events += 1
    pygame.time.set_timer(pygame.USEREVENT + user_events, 17000)
    pygame.mixer.music.play(loops=1)
    whistle_start_sound.play()
    scores = [[i, 0] for i in range(controller_count)]

    game_ended = False
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

            if event.type == pygame.USEREVENT + user_events:
                pygame.mixer.music.stop()
                whistle_end_sound.play()
                time.sleep(2)
                game_ended = True
                running = False
                break

        if not running:
            break

        buttons = get_wiimote_button_presses(wiimotes)

        if buttons[0].count('Home') > 0:
            break

        screen.fill((255, 255, 255))

        screen.blit(background, (0, 0))

        for border in border_positions:
            pygame.draw.line(screen, (0, 0, 0), border[0], border[1], width // 500)

        for section in range(controller_count):
            width_start = (selection_width * section)
            screen.blit(punching_bag, (width_start + (selection_width // 2 - punching_bag_width // 2), 0))

            if hand_location[section] == '2':
                screen.blit(gloves[0], (width_start + (selection_width // 15), height - (gloves[0].get_height())))
                screen.blit(gloves[3], (width_start + (selection_width * 2 // 15) + (gloves[0].get_width()), height - (gloves[3].get_height() * 2)))

                if 'A' in buttons[section] and '2' not in buttons[section]:
                    hand_location[section] = 'A'
                    punch_sound.play()
                    scores[section][1] += 1
            elif hand_location[section] == 'A':
                screen.blit(gloves[2], (width_start + (selection_width // 15), height - (gloves[3].get_height() * 2)))
                screen.blit(gloves[1], (width_start + (selection_width * 2 // 15) + (gloves[0].get_width()), height - (gloves[0].get_height())))

                if '2' in buttons[section] and 'A' not in buttons[section]:
                    hand_location[section] = '2'
                    punch_sound.play()
                    scores[section][1] += 1
            else:
                screen.blit(gloves[0], (width_start + (selection_width // 15), height - (gloves[0].get_height())))
                screen.blit(gloves[1], (width_start + (selection_width * 2 // 15) + (gloves[0].get_width()),
                            height - (gloves[0].get_height())))

                if '2' in buttons[section]:
                    hand_location[section] = '2'
                    punch_sound.play()
                    scores[section][1] += 1
                elif 'A' in buttons[section]:
                    hand_location[section] = 'A'
                    punch_sound.play()
                    scores[section][1] += 1

        pygame.display.flip()
        clock.tick(speed)

    if game_ended:
        return sorted(scores, key=lambda x: x[1], reverse=True)
