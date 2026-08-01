
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

