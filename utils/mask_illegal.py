
def mask_illegal(legal_actions: list, game_state: dict) -> list:
    if not legal_actions: return ["pass"]
    filtered = []
    my_bench = game_state.get("my_bench", [])
    my_deck_count = game_state.get("my_deck_count", 60)
    for action in legal_actions:
        if action.startswith("retreat:") and not my_bench: continue
        if action.startswith("play_trainer:"):
            trainer_name = action.split(":", 1)[1].lower() if ":" in action else ""
            draw_keywords = {"research", "professor", "carmine", "lillie", "colress"}
            shuffle_keywords = {"iono", "judge"}
            # Hard-prune draw supporters if deck count is <= 5
            if my_deck_count <= 5 and any(k in trainer_name for k in draw_keywords):
                continue
            # Hard-prune all draw/shuffle supporters if deck count is <= 3
            if my_deck_count <= 3 and any(k in trainer_name for k in draw_keywords | shuffle_keywords):
                continue
        filtered.append(action)
    return filtered or ["pass"]


def mask_illegal(legal_actions: list, game_state: dict) -> list:
    if not legal_actions: return ["pass"]
    filtered = []
    my_bench = game_state.get("my_bench", [])
    my_hand = game_state.get("my_hand", [])
    my_deck_count = game_state.get("my_deck_count", 60)
    for action in legal_actions:
        if action.startswith("retreat:") and not my_bench: continue
        # Removed aggressive stripping of attach_energy so the bot can attach energy
        if action.startswith("play_trainer:") and my_deck_count <= 0:
            trainer_name = action.split(":", 1)[1].lower() if ":" in action else ""
            if any(k in trainer_name for k in ["research", "iono", "judge", "draw"]): continue
        filtered.append(action)
    return filtered or ["pass"]


def mask_illegal(legal_actions: list, game_state: dict) -> list:
    if not legal_actions: return ["pass"]
    filtered = []
    my_bench = game_state.get("my_bench", [])
    my_deck_count = game_state.get("my_deck_count", 60)
    for action in legal_actions:
        if action.startswith("retreat:") and not my_bench: continue
        if action.startswith("play_trainer:"):
            trainer_name = action.split(":", 1)[1].lower() if ":" in action else ""
            draw_keywords = {"research", "professor", "carmine", "lillie", "colress"}
            shuffle_keywords = {"iono", "judge"}
            # Hard-prune draw supporters if deck count is <= 5
            if my_deck_count <= 5 and any(k in trainer_name for k in draw_keywords):
                continue
            # Hard-prune all draw/shuffle supporters if deck count is <= 3
            if my_deck_count <= 3 and any(k in trainer_name for k in draw_keywords | shuffle_keywords):
                continue
        filtered.append(action)
    return filtered or ["pass"]

