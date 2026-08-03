import os
from typing import List

def get_games(input_dir: str) -> List[dict]:
    """Loads all game replay JSONs from a directory, walking subdirectories.

    Args:
        input_dir: The root directory to search for .json replay files.

    Returns:
        A list of dictionaries, each representing a loaded game replay.
    """
    game_files = []
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.endswith(".json"):
                game_files.append(os.path.join(root, file))

    with ProcessPoolExecutor() as executor:
        games = list(executor.map(_load_json, game_files))

    return [g for g in games if g is not None]

