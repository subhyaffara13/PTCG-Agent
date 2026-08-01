
def fell_off(player_position):
    """Checks to see if the player_position means the player has fallen of the cliff."""
    return (
        (player_position[0] == 3)
        * (player_position[1] >= 1)
        * (player_position[1] <= 10)
    )

