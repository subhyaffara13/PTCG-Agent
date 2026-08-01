
def _get_player_idx(steps, info, team_names, name_or_id) -> int:
    if str(name_or_id).isdigit():
        if len(steps) > 1:
            for idx, p_state in enumerate(steps[1]):
                obs = p_state.get("observation") or {} if p_state else {}
                players = (obs.get("current") or {}).get("players", [])
                if idx < len(players) and str(players[idx].get("teamId")) == str(name_or_id):
                    return idx
    else:
        for idx, name in enumerate(team_names):
            if name_or_id.lower() in name.lower():
                return idx
    return -1

