from . import Dict

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

def _calc_sig(action: str, bench_sigs: Dict[int, str], gs: dict) -> str:
    parts = action.split(":")
    if len(parts) < 2:
        return action
    target = parts[1]
    if target.startswith("bench_"):
        try:
            idx = int(target.split("_")[1])
            if idx in bench_sigs:
                return f"{parts[0]}:bench_sig_{bench_sigs[idx]}"
        except (ValueError, IndexError):
            pass
    return action

