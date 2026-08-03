from typing import Any

def _inject_multi_game_context(observation: Mapping[str, Any]) -> str:
    """Status block shown only on the second and later games.

    On the first game (single-game session or game 0 of a multi-game session)
    the score is trivially 0–0 and nothing useful would be added, so the
    single-game prompt remains unchanged.
    """
    current_game = observation.get("current_game", 0)
    if current_game == 0:
        return ""

    blue_wins = observation.get("blue_wins", 0)
    yellow_wins = observation.get("yellow_wins", 0)
    return (
        f"This is game {current_game + 1}. The team with the most game wins "
        f"overall is the winner. Current score: BLUE {blue_wins} – "
        f"YELLOW {yellow_wins}.\n\n"
    )

