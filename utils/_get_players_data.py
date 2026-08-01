
def _get_players_data(players_state):
    if len(players_state) < 2 or not isinstance(players_state[0], dict) or not isinstance(players_state[1], dict):
        return []
    obs = players_state[0].get("observation") or {}
    curr = obs.get("current") or {}
    return curr.get("players", []) or []

