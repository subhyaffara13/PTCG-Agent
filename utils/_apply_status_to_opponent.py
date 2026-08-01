
def _apply_status_to_opponent(gs: dict, attack_name: str) -> None:
    """Apply status conditions based on attack flavor text keywords."""
    an = attack_name.lower() if attack_name else ""
    if "poison" in an or "toxic" in an:
        gs["opponent_active_status"] = "poisoned"
    if "burn" in an:
        gs["opponent_active_status"] = "burned"
    if "sleep" in an or "spore" in an or "drowsy" in an:
        gs["opponent_active_status"] = "asleep"
    if "paralyze" in an or "stun" in an or "thunder wave" in an:
        gs["opponent_active_status"] = "paralyzed"
    if "confuse" in an or "tear" in an:
        gs["opponent_active_status"] = "confused"


def _apply_status_to_opponent(gs: dict, attack_name: str) -> None:
    """Apply status conditions based on attack flavor text keywords."""
    an = attack_name.lower() if attack_name else ""
    if "poison" in an or "toxic" in an:
        gs["opponent_active_status"] = "poisoned"
    if "burn" in an:
        gs["opponent_active_status"] = "burned"
    if "sleep" in an or "spore" in an or "drowsy" in an:
        gs["opponent_active_status"] = "asleep"
    if "paralyze" in an or "stun" in an or "thunder wave" in an:
        gs["opponent_active_status"] = "paralyzed"
    if "confuse" in an or "tear" in an:
        gs["opponent_active_status"] = "confused"

