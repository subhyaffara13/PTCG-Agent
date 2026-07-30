def _score_combo_bonus(action, game_state):
from cb_agents.turn_planner_heuristics import _registry
    bonus = 0
    if ":" not in action:
        return bonus
    parts = action.split(":", 2)
    card_id = parts[1]
    if not card_id.isdigit():
        return bonus
    try:
        c = _registry.get(int(card_id))
        profile = game_state.get("priority_profile", "aggro_push")
        if c and c.combo_tags:
            if profile == "setup" and any(t in ("search", "bench", "setup") for t in c.combo_tags):
                bonus -= 4
            elif profile in ("aggro_push", "closing") and any(t in ("damage", "discard", "boss") for t in c.combo_tags):
                bonus -= 4
    except Exception: pass
    return bonus
