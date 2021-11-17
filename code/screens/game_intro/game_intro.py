import time
import pygame

from code.modules import global_vars
from code.helper_functions.call_game import call_game


def game_intro(game_number):
    width, height, screen, clock, speed, user_events = global_vars.width, global_vars.height, global_vars.screen, global_vars.clock, global_vars.speed, global_vars.user_events

    background = pygame.transform.smoothscale(pygame.image.load(f"content/main_screen/textures/game_pictures/{game_number}.png"), (width, height))
    intro_font = pygame.font.Font('content/global/fonts/Minercraftory.ttf', 7 * height // 9)

    pygame.mixer.music.load("content/global/sounds/start.mp3")

    text_time = 200
    appearance_times = [
        (1903, intro_font.render('3', True, (0, 0, 0))),
        (2914, intro_font.render('2', True, (0, 0, 0))),
        (3926, intro_font.render('1', True, (0, 0, 0))),
        (4870, intro_font.render('GO!', True, (0, 0, 0)))
    ]

    focus = None

    added_user_events = len(appearance_times)

    for appearance_time in range(len(appearance_times)):
        pygame.time.set_timer(pygame.USEREVENT + user_events + appearance_time + 1,
                              appearance_times[appearance_time][0], loops=1)

    pygame.mixer.music.play()
    added_user_events += 1
    stop_music_event = pygame.USEREVENT + user_events + added_user_events
    pygame.time.set_timer(stop_music_event, 6300, loops=1)
    beginning = True

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break

            for event_time in range(len(appearance_times)):
                if event.type == pygame.USEREVENT + user_events + event_time + 1:
                    focus = event_time
                    added_user_events += 1
                    pygame.time.set_timer(pygame.USEREVENT + user_events + added_user_events, text_time, loops=1)

            if event.type == pygame.USEREVENT + user_events + added_user_events:
                focus = None

            if event.type == stop_music_event:
                running = False

        screen.fill((255, 255, 255))

        screen.blit(background, (0, 0))
        if focus is not None:
            screen.blit(appearance_times[focus][1], (width // 2 - appearance_times[focus][1].get_width() // 2, height // 2 - appearance_times[focus][1].get_height() // 2))

        pygame.display.flip()

        clock.tick(speed)

    global_vars.user_events += added_user_events
    return call_game(game_number)
