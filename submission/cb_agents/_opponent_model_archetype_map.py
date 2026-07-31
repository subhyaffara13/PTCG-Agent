KEY_ID_TO_ARCHETYPE = {
    "721": "aggro",
    "722": "aggro",
    "979": "aggro",
    "1145": "stall",
    "1163": "stall",
    "1121": "control",
    "1262": "combo",
    "1260": "combo",
}

def predict_opponent_action(archetype: str, prizes_remaining: int, turn_number: int) -> str:
    if archetype == "aggro":
        return "attack" if prizes_remaining < 6 else "attach_energy"
    elif archetype == "control":
        return "play_trainer_disruption" if prizes_remaining <= 3 else "setup"
    elif archetype == "combo":
        return "execute_combo" if turn_number >= 3 else "setup_bench"
    return "unknown"
