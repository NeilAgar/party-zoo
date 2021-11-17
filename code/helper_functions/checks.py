from code.modules.wiimotes import wiimote_initializer


def wiimote_number_check(wiimote_count):
    if not (wiimote_count > 4 or wiimote_count < 2):
        return wiimote_initializer()

    print("Wiimote count not valid (2 - 4 players only)")
