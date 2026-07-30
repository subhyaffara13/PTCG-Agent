from . import CardRegistry, _registry, logger

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

def _parse_damage_str(move_name: str) -> int:
    import re
    dmg_str = _registry.move_damage.get(move_name, "0")
    try:
        match = re.match(r"^(\d+)", dmg_str)
        if match:
            return int(match.group(1))
    except Exception:
        pass
    return 0
