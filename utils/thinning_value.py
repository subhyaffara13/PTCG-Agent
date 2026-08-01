
def thinning_value(candidate: str, game_state: dict) -> float:
    if not candidate.startswith("play_trainer:"): return 0.0
    name = candidate.split(":", 1)[1].lower()
    if not any(sk in name for sk in _SEARCH_KEYWORDS): return 0.0
    dc = game_state.get("my_deck_count", 60)
    return 0.3 if dc > 45 else (0.15 if dc > 30 else 0.0)


def thinning_value(candidate: str, game_state: dict) -> float:
    if not candidate.startswith("play_trainer:"): return 0.0
    name = candidate.split(":", 1)[1].lower()
    if not any(sk in name for sk in _SEARCH_KEYWORDS): return 0.0
    dc = game_state.get("my_deck_count", 60)
    return 0.3 if dc > 45 else (0.15 if dc > 30 else 0.0)


def thinning_value(candidate: str, game_state: dict) -> float:
    if not candidate.startswith("play_trainer:"): return 0.0
    name = candidate.split(":", 1)[1].lower()
    if not any(sk in name for sk in _SEARCH_KEYWORDS): return 0.0
    dc = game_state.get("my_deck_count", 60)
    return 0.3 if dc > 45 else (0.15 if dc > 30 else 0.0)

