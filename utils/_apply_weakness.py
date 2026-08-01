
def _apply_weakness(damage: int, my_active_id, opp_active_id) -> int:
    try:
        if my_active_id is not None and opp_active_id is not None:
            my_type = _registry.card_poke_type.get(int(my_active_id), "")
            opp_weakness = _registry.card_weakness.get(int(opp_active_id), "")
            if my_type and opp_weakness and my_type.lower() == opp_weakness.lower():
                return damage * 2
    except Exception:
        pass
    return damage


def _apply_weakness(damage: int, my_active_id, opp_active_id) -> int:
    try:
        if my_active_id is not None and opp_active_id is not None:
            my_type = _registry.card_poke_type.get(int(my_active_id), "")
            opp_weakness = _registry.card_weakness.get(int(opp_active_id), "")
            if my_type and opp_weakness and my_type.lower() == opp_weakness.lower():
                return damage * 2
    except Exception:
        pass
    return damage

