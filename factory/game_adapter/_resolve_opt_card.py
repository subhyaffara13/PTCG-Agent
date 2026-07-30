from . import _registry

def _resolve_card_id(opt, current, p_idx):
    card_id = opt.get("id")
    if card_id is not None:
        return card_id
    area = opt.get("area")
    index = opt.get("index")
    if current is None:
        return None
    players = current.get("players", [])
    if not (len(players) > p_idx and players[p_idx] is not None):
        return None
    p_state = players[p_idx]
    if area == 2:
        hand = p_state.get("hand", [])
        if len(hand) > index:
            return hand[index].get("id")
    elif area == 12:
        bench = p_state.get("bench", [])
        if len(bench) > index:
            return bench[index].get("id")
    elif area == 4:
        active = p_state.get("active", [])
        if len(active) > index:
            return active[index].get("id")
    return None

def _resolve_instance(val):
    if isinstance(val, list):
        return val[0] if len(val) > 0 else None
    return val
