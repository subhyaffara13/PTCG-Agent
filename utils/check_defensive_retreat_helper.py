
def check_defensive_retreat_helper(game_state, board_summary) -> str:
    dmg_info = project_opponent_damage_helper(game_state)
    opponent_max_damage = dmg_info["max_damage"]
    opponent_type = dmg_info.get("opponent_type", "")
    my_hp = getattr(game_state, 'my_active_hp', 0)
    retreat_actions = list(getattr(game_state, 'legal_retreats', []))
    if not retreat_actions:
        return None
    # One-shot lethal: strong retreat push
    if opponent_max_damage > 0 and opponent_max_damage >= my_hp:
        return _best_retreat_target(retreat_actions, game_state, opponent_max_damage, opponent_type)
    # Preemptive 2HKO: softer retreat suggestion (lets other actions compete)
    if dmg_info.get("can_2hko") and my_hp <= opponent_max_damage * 1.8:
        return _best_retreat_target(retreat_actions, game_state, opponent_max_damage, opponent_type)
    return None


def check_defensive_retreat_helper(game_state, board_summary) -> str:
    opponent_max_damage = project_opponent_damage_helper(game_state)
    my_hp = getattr(game_state, 'my_active_hp', 0)
    if opponent_max_damage > 0 and opponent_max_damage >= my_hp:
        retreat_actions = list(getattr(game_state, 'legal_retreats', []))
        if retreat_actions:
            return retreat_actions[0]
    return None


def check_defensive_retreat_helper(game_state, board_summary) -> str:
    dmg_info = project_opponent_damage_helper(game_state)
    opponent_max_damage = dmg_info["max_damage"]
    opponent_type = dmg_info.get("opponent_type", "")
    my_hp = getattr(game_state, 'my_active_hp', 0)
    retreat_actions = list(getattr(game_state, 'legal_retreats', []))
    if not retreat_actions:
        return None
    # One-shot lethal: strong retreat push
    if opponent_max_damage > 0 and opponent_max_damage >= my_hp:
        return _best_retreat_target(retreat_actions, game_state, opponent_max_damage, opponent_type)
    # Preemptive 2HKO: softer retreat suggestion (lets other actions compete)
    if dmg_info.get("can_2hko") and my_hp <= opponent_max_damage * 1.8:
        return _best_retreat_target(retreat_actions, game_state, opponent_max_damage, opponent_type)
    return None

