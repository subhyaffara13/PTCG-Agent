
def _apply_weakness_resistance(gs, actual_damage, CardRegistry, my_active_id):
    if actual_damage <= 0 or CardRegistry is None:
        return actual_damage
    try:
        registry = CardRegistry()
        if my_active_id is not None:
            atk_type = registry.card_poke_type.get(int(my_active_id) if not isinstance(my_active_id, int) else my_active_id, "")
        else:
            atk_type = ""
        opp_active = gs.get("opponent_active", {})
        opp_id = gs.get("opponent_active_id") or (opp_active.get("id") if isinstance(opp_active, dict) else None)
        if opp_id is not None:
            opp_id_int = int(opp_id) if not isinstance(opp_id, int) else opp_id
            opp_weakness = registry.card_weakness.get(opp_id_int, "")
            opp_resistance = registry.card_resistance.get(opp_id_int, "")
            if atk_type and opp_weakness and atk_type == opp_weakness:
                actual_damage *= 2
            if atk_type and opp_resistance and atk_type == opp_resistance:
                actual_damage = max(0, actual_damage - 30)
    except Exception: pass
    return actual_damage


def _apply_weakness_resistance(damage: int, atk_type: str, defender_id, registry) -> int:
    """Apply weakness (2x) and resistance (-30) to raw damage."""
    if not atk_type or defender_id is None or damage <= 0:
        return damage
    try:
        def_id = int(defender_id) if not isinstance(defender_id, int) else defender_id
        weak = registry.card_weakness.get(def_id, "")
        resist = registry.card_resistance.get(def_id, "")
        if atk_type and weak and atk_type == weak:
            damage *= 2
        if atk_type and resist and atk_type == resist:
            damage = max(0, damage - 30)
    except Exception:
        pass
    return damage


def _apply_weakness_resistance(gs, actual_damage, CardRegistry, my_active_id):
    if actual_damage <= 0 or CardRegistry is None:
        return actual_damage
    try:
        registry = CardRegistry()
        if my_active_id is not None:
            atk_type = registry.card_poke_type.get(int(my_active_id) if not isinstance(my_active_id, int) else my_active_id, "")
        else:
            atk_type = ""
        opp_active = gs.get("opponent_active", {})
        opp_id = gs.get("opponent_active_id") or (opp_active.get("id") if isinstance(opp_active, dict) else None)
        if opp_id is not None:
            opp_id_int = int(opp_id) if not isinstance(opp_id, int) else opp_id
            opp_weakness = registry.card_weakness.get(opp_id_int, "")
            opp_resistance = registry.card_resistance.get(opp_id_int, "")
            if atk_type and opp_weakness and atk_type == opp_weakness:
                actual_damage *= 2
            if atk_type and opp_resistance and atk_type == opp_resistance:
                actual_damage = max(0, actual_damage - 30)
    except Exception: pass
    return actual_damage


def _apply_weakness_resistance(damage: int, atk_type: str, defender_id, registry) -> int:
    """Apply weakness (2x) and resistance (-30) to raw damage."""
    if not atk_type or defender_id is None or damage <= 0:
        return damage
    try:
        def_id = int(defender_id) if not isinstance(defender_id, int) else defender_id
        weak = registry.card_weakness.get(def_id, "")
        resist = registry.card_resistance.get(def_id, "")
        if atk_type and weak and atk_type == weak:
            damage *= 2
        if atk_type and resist and atk_type == resist:
            damage = max(0, damage - 30)
    except Exception:
        pass
    return damage

