from . import _registry

def _detect_is_discard(select, observation):
    sel_type = select.get("type")
    if sel_type not in (1, 2, 4):
        return False
    if sel_type == 4 or str(select.get("context", "")).lower() in ("discard", "energy_discard"):
        return True
    current = observation.get("current")
    if current is None:
        return False
    my_idx = current.get("yourIndex", 0)
    players = current.get("players", [])
    if not (len(players) > my_idx and players[my_idx] is not None):
        return False
    my_hand_ids = [c.get("id") for c in players[my_idx].get("hand", []) if c and c.get("id") is not None]
    option_card_ids = []
    opts = select.get("options") or select.get("option") or []
    for opt in opts:
        opt_id = opt.get("id")
        if opt_id is None:
            area = opt.get("area")
            index = opt.get("index")
            p_idx = opt.get("playerIndex", 0)
            if p_idx == my_idx and area == 2:
                hand = players[my_idx].get("hand", [])
                if len(hand) > index:
                    opt_id = hand[index].get("id")
        if opt_id is not None:
            option_card_ids.append(opt_id)
    return bool(option_card_ids and all(oid in my_hand_ids for oid in option_card_ids))
