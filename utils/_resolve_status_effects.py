import random

def _resolve_status_effects(gs: dict) -> None:
    """Apply status condition tick effects at turn start/end (poison/burn)."""
    status = gs.get("my_active_status", "")
    if status == "poisoned":
        hp = gs.get("my_active_hp", 100)
        gs["my_active_hp"] = max(0, hp - 10)
    elif status == "burned":
        hp = gs.get("my_active_hp", 100)
        gs["my_active_hp"] = max(0, hp - 20)
    elif status == "asleep":
        # Sleep recovery: 50% chance to wake (simplified: 1 turn)
        if random.random() < 0.5:
            gs["my_active_status"] = ""
    elif status == "confused":
        # Confusion recovery: 50% chance per turn
        if random.random() < 0.5:
            gs["my_active_status"] = ""
    elif status == "paralyzed":
        # Paralyzed: Pokemon can't attack this turn
        if random.random() < 0.5:
            gs["my_active_status"] = ""
        gs["turn_ended"] = True

    # Apply same for opponent status
    opp_status = gs.get("opponent_active_status", "")
    if opp_status == "poisoned":
        gs["opponent_active_hp"] = max(0, gs.get("opponent_active_hp", 100) - 10)
    elif opp_status == "burned":
        gs["opponent_active_hp"] = max(0, gs.get("opponent_active_hp", 100) - 20)
    elif opp_status == "asleep":
        if random.random() < 0.5:
            gs["opponent_active_status"] = ""
    elif opp_status == "confused":
        if random.random() < 0.5:
            gs["opponent_active_status"] = ""
    elif opp_status == "paralyzed":
        if random.random() < 0.5:
            gs["opponent_active_status"] = ""
        gs["opponent_skip_turn"] = True


def _resolve_status_effects(gs: dict) -> None:
    """Apply status condition tick effects at turn start/end (poison/burn)."""
    status = gs.get("my_active_status", "")
    if status == "poisoned":
        hp = gs.get("my_active_hp", 100)
        gs["my_active_hp"] = max(0, hp - 10)
    elif status == "burned":
        hp = gs.get("my_active_hp", 100)
        gs["my_active_hp"] = max(0, hp - 20)
    elif status == "asleep":
        # Sleep recovery: 50% chance to wake (simplified: 1 turn)
        if random.random() < 0.5:
            gs["my_active_status"] = ""
    elif status == "confused":
        # Confusion recovery: 50% chance per turn
        if random.random() < 0.5:
            gs["my_active_status"] = ""
    elif status == "paralyzed":
        # Paralyzed: Pokemon can't attack this turn
        if random.random() < 0.5:
            gs["my_active_status"] = ""
        gs["turn_ended"] = True

    # Apply same for opponent status
    opp_status = gs.get("opponent_active_status", "")
    if opp_status == "poisoned":
        gs["opponent_active_hp"] = max(0, gs.get("opponent_active_hp", 100) - 10)
    elif opp_status == "burned":
        gs["opponent_active_hp"] = max(0, gs.get("opponent_active_hp", 100) - 20)
    elif opp_status == "asleep":
        if random.random() < 0.5:
            gs["opponent_active_status"] = ""
    elif opp_status == "confused":
        if random.random() < 0.5:
            gs["opponent_active_status"] = ""
    elif opp_status == "paralyzed":
        if random.random() < 0.5:
            gs["opponent_active_status"] = ""
        gs["opponent_skip_turn"] = True

