
def find_player_idx_in_steps(steps, player_name_or_id):
    player_idx = -1
    if str(player_name_or_id).isdigit():
        if len(steps) > 1:
            for idx, p_state in enumerate(steps[1]):
                obs_dict = p_state.get("observation") or {} if p_state else {}
                current = obs_dict.get("current") or {} if obs_dict else {}
                players = current.get("players", []) if current else []
                if idx < len(players) and str(players[idx].get("teamId")) == str(player_name_or_id):
                    player_idx = idx
                    break
    else:
        info = steps[0] if steps else {}
        team_names = info.get("TeamNames", []) if isinstance(info, dict) else ["", ""]
        for idx, name in enumerate(team_names):
            if player_name_or_id.lower() in name.lower():
                player_idx = idx
                break
    return player_idx

