def _extract_state_action(step: dict) -> tuple:
    if not isinstance(step, dict):
        return {}, ""
    players = step.get("players") or []
    if len(players) < 2:
        return {}, ""
        
    p0 = players[0]
    p1 = players[1]
    
    # Active player is the one with select
    if p0.get("observation", {}).get("select") is not None:
        active_player = p0
    elif p1.get("observation", {}).get("select") is not None:
        active_player = p1
    else:
        return {}, ""
        
    raw_action = active_player.get("action")
    if not raw_action or not isinstance(raw_action, list):
        return {}, ""
        
    obs = active_player.get("observation") or {}
    if not isinstance(obs, dict):
        obs = {}
    select = obs.get("select") or {}
    options = select.get("option") or []
    opt_idx = raw_action[0]
    if not (0 <= opt_idx < len(options)):
        return {}, ""
        
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
        
    # Decode raw action list [idx] to string representation
    opt = options[opt_idx]
    opt_type = opt.get("type")
    
    action_str = ""
    if opt_type == 14:
        action_str = "pass"
    elif opt_type in (12, 13):
        action_str = "attack:0"
    elif opt_type in (10, 12):
        action_str = "retreat:0"
    elif opt_type in (7, 8):
        hand_idx = opt.get("index", -1)
        hand = obs_player.get("hand", [])
        if 0 <= hand_idx < len(hand):
            card_obj = hand[hand_idx]
            card_id = card_obj.get("id") if isinstance(card_obj, dict) else card_obj
            if card_id:
                if opt_type == 8:
                    action_str = f"bench:{card_id}"
                else:
                    from agents.card_registry import CardRegistry
                    from agents.card_types import CardType
                    registry = CardRegistry()
                    card_entry = registry.get(card_id)
                    if card_entry and card_entry.card_type == CardType.ENERGY:
                        action_str = f"attach_energy:{card_id}"
                    else:
                        action_str = f"play_trainer:{card_id}"
                        
    state_dict = {
        "hand": _pluck("hand"),
        "active": (obs_player.get("active", [None]) or [None])[0].get("id") if isinstance((obs_player.get("active") or [None])[0], dict) else -1,
        "bench": _pluck("bench"),
        "prize": obs_player.get("prize", []),
        "opponent_visible": [],
        "turn": current.get("turn", 1),
        "is_first_player": 1 if current.get("yourIndex", 0) == 0 else 0,
    }
    
    return state_dict, action_str

def _extract_all_steps(steps_data: list, aligner) -> tuple:
    states, actions = [], []
    for step in steps_data:
        flat_state, raw_action = _extract_state_action(step)
        states.append(aligner.normalize_state(flat_state))
        actions.append(aligner.normalize_action(raw_action))
    return states, actions
