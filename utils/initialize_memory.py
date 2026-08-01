
def initialize_memory(observation, board_size):
    """Initializes memory fields if not present."""
    if "history" not in observation:
        observation.history = []
        observation.current_game = 0
        observation.blue_wins = 0
        observation.yellow_wins = 0
        observation.current_game_turns = []
        observation._last_clue = ""
        observation._last_revealed = [False] * board_size

