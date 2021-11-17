import time

from code.modules import global_vars
from code.modules.wiimotes import *
from code.screens.main_screen.character_select import character_select


def title():
    width, height, screen, clock, speed, character_colors, wiimotes, already_pressed, total_characters = global_vars.width, global_vars.height, global_vars.screen, global_vars.clock, global_vars.speed, global_vars.character_colors, global_vars.wiimotes, global_vars.already_pressed, global_vars.total_characters
    title_font = pygame.font.Font('content/global/fonts/Minercraftory.ttf', 2*height//9)
    title_text = title_font.render('Party Zoo', True, (0, 0, 0))

    background = pygame.transform.scale(pygame.image.load("content/main_screen/textures/title_background.png"), (width, height))
    play_button = pygame.image.load("content/main_screen/textures/play_button.png")
    greyed_play_button = pygame.image.load("content/main_screen/textures/greyed_play_button.png")
    characters = [pygame.transform.scale(pygame.image.load(f"content/main_screen/textures/characters/{i}.png"), (3*height // 10, 3*height // 10)) for i in range(0, total_characters)] + [title_text]

    intro = pygame.mixer.Sound("content/main_screen/sounds/intro_music.mp3")

    pygame.mixer.music.load("content/main_screen/sounds/background_music.mp3")

    character_times = [
        [pygame.USEREVENT + i for i in range(0, total_characters + 1)],
        [4376, 6050, 7660, 8066, 8478, 9150, 9696, 10050, 10400, 15500],
        [(width//5-characters[0].get_width()//2, height//2),
         (width*4//5-characters[1].get_width()//2, height//2),
         (width//3-characters[0].get_width()//2, height//2),
         (width*2//3-characters[0].get_width()//2, height//2),
         (width//6-characters[2].get_width()//2, height*3//4-characters[2].get_height()//2),
         (width*2//6-characters[3].get_width()//2, height*3//4-characters[3].get_height()//2),
         (width//2-characters[4].get_width()//2, height*3//4-characters[4].get_height()//2),
         (width*2//3-characters[5].get_width()//2, height*3//4-characters[5].get_height()//2),
         (width*5//6-characters[6].get_width()//2, height*3//4-characters[6].get_height()//2),
         (width // 2-title_text.get_width()//2, height // 6-title_text.get_height()//2)
        ]
    ]

    global_vars.user_events += total_characters + 1

    for timer in range(len(character_times[0])):
        pygame.time.set_timer(character_times[0][timer], character_times[1][timer])

    used_characters = []

    intro_over = False
    event_over = False

    intro.play()

    play_opened = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break

            if event.type in character_times[0] and event.type not in used_characters:
                used_characters.append(event.type)

        # buttons = get_individual_buttons(get_wiimote_button_presses(wiimotes), already_pressed)
        buttons = get_wiimote_button_presses(wiimotes)

        if buttons[0].count('Home') > 0:
            break

        if not pygame.mixer.get_busy() and not intro_over:
            time.sleep(2)
            pygame.mixer.music.play(loops=-1, fade_ms=3000)
            intro_over = True

        screen.fill((255, 255, 255))

        screen.blit(background, (0, 0))

        if len(used_characters) > total_characters:
            pygame.draw.rect(screen, character_colors[0], pygame.Rect(width//2-play_button.get_width()//2-10, height//2-play_button.get_height()//2-10, play_button.get_width()+20, play_button.get_height()+20))
            screen.blit(play_button, (width // 2 - play_button.get_width() // 2, height // 2 - play_button.get_height() // 2))
            if buttons[0].count('2') > 0:
                play_opened = True
                break

        else:
            screen.blit(greyed_play_button, (width//2-play_button.get_width()//2, height//2-play_button.get_height()//2))

        for cube in range(len(used_characters)):
            screen.blit(characters[cube], character_times[2][cube])

        pygame.display.flip()

        clock.tick(speed)

    if play_opened:
        time.sleep(1)
        character_select()
