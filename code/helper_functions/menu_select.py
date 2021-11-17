def get_y_pos(spacing, picture_height, title_height, game_number):
    pos = spacing + title_height
    pos += spacing * (((game_number - 1) // 3) + 1)
    pos += picture_height * ((game_number - 1) // 3)
    return pos


def get_x_pos(spacing, picture_width, game_number):
    row = (game_number - 1) % 3
    pos = spacing * (row + 1)
    pos += picture_width * row
    return pos


def get_picture_positions(width_spacing, height_spacing, picture_width, picture_height, title_height, number_of_games):
    positions = []
    for num in range(1, number_of_games+1):
        positions.append(
            (get_x_pos(width_spacing, picture_width, num),
             get_y_pos(height_spacing, picture_height, title_height, num))
        )

    return positions
