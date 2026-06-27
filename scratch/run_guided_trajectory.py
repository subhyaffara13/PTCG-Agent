def _extract_state_action(step: dict) -> tuple:
    if not isinstance(step, dict):
        return {}, ""
    players = step.get("players") or []
    if not players or not isinstance(players, list):
        return {}, ""
    p0 = players[0]
    if not isinstance(p0, dict):
        return {}, ""
    raw_action = p0.get("action") or ""
    if not isinstance(raw_action, str):
        raw_action = ""
    obs = p0.get("observation") or {}
    if not isinstance(obs, dict):
        obs = {}
    current = obs.get("current") or {}
    if not isinstance(current, dict):
        current = {}
    all_players = current.get("players") or []
    if not isinstance(all_players, list):
        all_players = []
    if not all_players:
        obs_players = obs.get("players") or []
        obs_player = obs_players[0] if isinstance(obs_players, list) and obs_players else {}
    else:
        my_idx = current.get("yourIndex", 0)
        if not isinstance(my_idx, int):
            my_idx = 0
        obs_player = all_players[my_idx] if my_idx < len(all_players) else {}
    if not isinstance(obs_player, dict):
        obs_player = {}
    def _pluck(zone):
        items = obs_player.get(zone, [])
        return [c.get("id") if isinstance(c, dict) else c for c in items]
    return {
        "hand": _pluck("hand"),
        "active": (obs_player.get("active", [None]) or [None])[0].get("id") if isinstance((obs_player.get("active") or [None])[0], dict) else -1,
        "bench": _pluck("bench"),
        "prize": obs_player.get("prize", []),
        "opponent_visible": [],
        "turn": current.get("turn", 1),
        "is_first_player": 1 if current.get("yourIndex", 0) == 0 else 0,
    }, raw_action

def _extract_all_steps(steps_data: list, aligner) -> tuple:
    states, actions = [], []
    for step in steps_data:
        flat_state, raw_action = _extract_state_action(step)
        states.append(aligner.normalize_state(flat_state))
        actions.append(aligner.normalize_action(raw_action))
    return states, actions
