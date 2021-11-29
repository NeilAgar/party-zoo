from code.modules.wiimotes import wiimote_initializer


def wiimote_number_check(wiimote_count):
    if 0 <= wiimote_count <= 4:
        return wiimote_initializer()

    print("Wiimote count not valid (2 - 4 players only)")
