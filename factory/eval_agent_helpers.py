import logging

logger = logging.getLogger(__name__)

def determine_context(change_type: str, archetype: str) -> str:
    if change_type == "deck_swap": return "deck_test"
    if change_type == "strategy_patch":
        return "aggro_test" if archetype in ("aggro", "control", "combo", "utility") else "meta_test"
    return "micro_patch" if change_type == "micro_patch" else "aggro_test"

def score_game_metrics(game_logs: dict, weights: dict, logic_delta: float, theoretical_min_turns: int) -> float:
    data = game_logs.get("game_data", {})
    if not data or data.get("winner") == "error": return 0.0
    turns = max(1, data.get("turns_taken", 1))
    win_rate = 1.0 if data.get("winner") == "player_b" else 0.0
    prizes = data.get("prizes_taken_b", 0)
    
    return (
        win_rate * weights.get("win_rate", 0.0) +
        (prizes / turns) * weights.get("prize_efficiency", 0.0) +
        (theoretical_min_turns / turns) * weights.get("turn_efficiency", 0.0) +
        (1.0 if prizes > 0 else 0.0) * weights.get("ko_rate", 0.0) +
        logic_delta * weights.get("logic_delta", 0.0)
    )
