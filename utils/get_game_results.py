import os
from typing import List, Optional

def get_game_results(
    input_dir: str, preserve_full_record: bool = False, max_workers: Optional[int] = None
) -> List["GameResult"]:
    """Loads all game replays and returns GameResult objects, in parallel.

    Args:
        input_dir: The root directory to search for .json replay files.
        preserve_full_record: If True, keeps the entire game JSON in memory
            (useful for debugging but consumes significant RAM).
        max_workers: The maximum number of worker processes to use.

    Returns:
        A list of GameResult objects.
    """
    game_files = []
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.endswith(".json"):
                game_files.append(os.path.join(root, file))

    args = [(f, preserve_full_record) for f in game_files]
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(_load_game_result, args))

    return [r for r in results if r is not None]

