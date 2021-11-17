import pygame

from code.modules import global_vars
from code.modules.wiimotes import get_wiimote_button_presses, wiimote_initializer


def end_screen(positions):
    width, height, screen, clock, speed, players, character_assignment, placement_colors, user_events, character_colors = global_vars.width, global_vars.height, global_vars.screen, global_vars.clock, global_vars.speed, global_vars.controller_count, global_vars.character_assignment, global_vars.placement_colors, global_vars.user_events, global_vars.character_colors

    wiimotes = wiimote_initializer()

    background = pygame.transform.scale(pygame.image.load("content/end_screen/textures/background.png"), (width, height))

    starting_height = height//2
    height_placement_increment = starting_height//(players+1)

    placement_width = width // (players + 1)
    placement_heights = [starting_height - height_placement_increment * i for i in range(players)]
    placement_spacing = (width - placement_width * players) // (players + 1)
    placement_pos = [(placement_width * i + placement_spacing * (i + 1), height - placement_heights[i]) for i in range(players)]
    placement_rects = [pygame.Rect(placement_pos[i][0], placement_pos[i][1], placement_width, placement_heights[i]) for i in range(players)]

    user_width = placement_width * 2 // 3
    user_height = user_width
    user_pos = [(placement_pos[i][0] + placement_width // 2 - user_width // 2, height - user_height - placement_heights[i]) for i in range(players)]
    user_pictures = [pygame.transform.scale(pygame.image.load(f"content/main_screen/textures/characters/{character_assignment[positions[i][0]] - 1}.png"), (user_width, user_height)) for i in range(players)]

    placement_fonts = [pygame.font.Font('content/global/fonts/Minercraftory.ttf', placement_heights[i]//10) for i in range(players)]
    placement_texts = [placement_fonts[i].render(str(positions[i][1]), True, (255, 255, 255)) for i in range(players)]
    placement_text_pos = [(placement_pos[i][0] + placement_width // 2 - placement_texts[i].get_width() // 2, height - placement_heights[i]) for i in range(players)]

    button_images = [pygame.image.load(f"content/end_screen/textures/{i}.png") for i in ["greyed_play_again", "greyed_play_diff", "play_again", "play_diff"]]
    button_width = width // 2
    button_height = (button_width // button_images[0].get_width()) * button_images[0].get_height()
    button_images = [pygame.transform.scale(button_images[i], (button_width, button_height)) for i in range(len(button_images))]
    button_spacing = (height - button_height * len(button_images) // 2) // (len(button_images) // 2 + 1)

    highlight_rects = [pygame.Rect(width // 2 - button_width // 2 - width // 10, button_spacing * (i + 1) + button_height * i - button_spacing // 5, button_width + width // 5, button_height + button_spacing * 2 // 5) for i in range(len(button_images) // 2)]

    intro_sound = pygame.mixer.Sound("content/end_screen/sounds/intro.mp3")
    pygame.mixer.music.load("content/end_screen/sounds/background_music.mp3")

    global_vars.user_events += 1
    pygame.time.set_timer(pygame.USEREVENT + global_vars.user_events, 4000, loops=1)

    intro_sound.play()

    menu_overlay = False
    selection = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.USEREVENT + global_vars.user_events:
                menu_overlay = True
                pygame.mixer.music.play(fade_ms=750)

        buttons = get_wiimote_button_presses(wiimotes)

        if buttons[0].count('Home') > 0:
            break

        screen.fill((255, 255, 255))

        screen.blit(background, (0, 0))

        for player in range(players):
            pygame.draw.rect(screen, placement_colors[player], placement_rects[player])
            screen.blit(user_pictures[player], user_pos[player])
            screen.blit(placement_texts[player], placement_text_pos[player])

        if menu_overlay:
            pygame.draw.rect(screen, character_colors[0], highlight_rects[selection])
            for button in range(len(button_images) // 2):
                if button == selection:
                    screen.blit(button_images[button + len(button_images) // 2], (width // 2 - button_width // 2, button_spacing * (button + 1) + button_height * button))
                else:
                    screen.blit(button_images[button], (width // 2 - button_width // 2, button_spacing * (button + 1) + button_height * button))

            if selection < 1 and buttons[0].count('Down') > 0:
                selection = 1
            elif selection > 0 and buttons[0].count('Up') > 0:
                selection = 0
            if buttons[0].count('2') > 0:
                running = False
                break

        pygame.display.flip()

        clock.tick(speed)

    pygame.mixer.music.stop()

    if selection == 0:
        return True
