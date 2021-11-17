from code.screens.games.boxing.boxing import boxing


def call_game(game_number):
    if game_number == 0:
        return boxing()
