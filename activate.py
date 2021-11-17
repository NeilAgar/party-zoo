import pygame

from code.helper_functions.checks import wiimote_number_check
from code.helper_functions.get_config import get_config
from code.screens.main_screen.title import title
from code.modules.global_vars import init

# Checks + Adding Wiimotes

if not wiimote_number_check(get_config()[0]):
    quit()

print("Wiimotes added!")

init((get_config()[1][0], get_config()[1][1]), get_config()[0])

# Calling Title

title()
