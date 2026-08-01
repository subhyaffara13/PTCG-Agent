
def extract_prizes(p1_state: dict, p2_state: dict) -> tuple:
    prizes_a = prizes_b = 0
    try:
        players = p1_state.get("observation", {}).get("current", {}).get("players", [])
        if len(players) > 1:
            prizes_a = 6 - len(players[0].get("prize", []))
            prizes_b = 6 - len(players[1].get("prize", []))
    except Exception:
        pass
    return prizes_a, prizes_b

