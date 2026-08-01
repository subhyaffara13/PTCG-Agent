
def _score_attack(v: float, action: str, gs: dict, ac: dict, opp_hp: float, mp: int, ahp: int) -> float:
    if not action.startswith("attack:"):
        return v
    my_status = gs.get("my_active_status", "")
    is_stunned = my_status in ("paralyzed", "asleep")
    can_attack = not is_stunned
    if isinstance(ac, dict) and not is_stunned:
        attached_count = len(ac.get("attached", []) or ac.get("energies", []))
        active_id = ac.get("id")
        if active_id is not None:
            try:
                min_cost = _registry.get_min_energy_cost(active_id)
                can_attack = attached_count >= min_cost
            except Exception:
                can_attack = attached_count >= 1
        else:
            can_attack = attached_count >= 1
    if not can_attack:
        v -= 0.5 if not is_stunned else 0.8
    else:
        v += 0.65
    if my_status in ("poisoned", "burned"):
        v += 0.2
    if mp <= 1:
        v += 1.0
    if mp <= 2:
        v += 0.3
    opp_ac = gs.get("opponent_active_pokemon", {})
    if isinstance(ac, dict) and isinstance(opp_ac, dict):
        my_type = ac.get("element_type", "")
        opp_weak = opp_ac.get("weakness", "")
        has_weakness = my_type and opp_weak and my_type.lower() == opp_weak.lower()
        if has_weakness:
            v += 0.8
    if isinstance(ac, dict) and not is_stunned:
        my_active_id = ac.get("id")
        if my_active_id is not None:
            try:
                card = _registry.get_full_skill(my_active_id)
                if card:
                    effective_dmg = card.damage_output
                    my_type_str = ac.get("element_type", "")
                    opp_weak_str = opp_ac.get("weakness", "") if isinstance(opp_ac, dict) else ""
                    if my_type_str and opp_weak_str and my_type_str.lower() == opp_weak_str.lower():
                        effective_dmg *= 2
                    if effective_dmg >= opp_hp:
                        v += 1.5
            except Exception as e:
                logger.debug(f"KO check registry error: {e}")
    opp_status = gs.get("opponent_active_status", "")
    if opp_status in ("asleep", "paralyzed"):
        v += 0.4
    elif opp_status in ("poisoned", "burned", "confused"):
        v += 0.15
    return v


def _score_attack(v: float, action: str, gs: dict, ac: dict, opp_hp: float, mp: int, ahp: int) -> float:
    if not action.startswith("attack:"):
        return v
    my_status = gs.get("my_active_status", "")
    is_stunned = my_status in ("paralyzed", "asleep")
    can_attack = not is_stunned
    if isinstance(ac, dict) and not is_stunned:
        attached_count = len(ac.get("attached", []) or ac.get("energies", []))
        active_id = ac.get("id")
        if active_id is not None:
            try:
                min_cost = _registry.get_min_energy_cost(active_id)
                can_attack = attached_count >= min_cost
            except Exception:
                can_attack = attached_count >= 1
        else:
            can_attack = attached_count >= 1
    if not can_attack:
        v -= 0.5 if not is_stunned else 0.8
    else:
        v += 0.65
    if my_status in ("poisoned", "burned"):
        v += 0.2
    if mp <= 1:
        v += 1.0
    if mp <= 2:
        v += 0.3
    opp_ac = gs.get("opponent_active_pokemon", {})
    if isinstance(ac, dict) and isinstance(opp_ac, dict):
        my_type = ac.get("element_type", "")
        opp_weak = opp_ac.get("weakness", "")
        has_weakness = my_type and opp_weak and my_type.lower() == opp_weak.lower()
        if has_weakness:
            v += 0.8
    if isinstance(ac, dict) and not is_stunned:
        my_active_id = ac.get("id")
        if my_active_id is not None:
            try:
                card = _registry.get_full_skill(my_active_id)
                if card:
                    effective_dmg = card.damage_output
                    my_type_str = ac.get("element_type", "")
                    opp_weak_str = opp_ac.get("weakness", "") if isinstance(opp_ac, dict) else ""
                    if my_type_str and opp_weak_str and my_type_str.lower() == opp_weak_str.lower():
                        effective_dmg *= 2
                    if effective_dmg >= opp_hp:
                        v += 1.5
            except Exception as e:
                logger.debug(f"KO check registry error: {e}")
    opp_status = gs.get("opponent_active_status", "")
    if opp_status in ("asleep", "paralyzed"):
        v += 0.4
    elif opp_status in ("poisoned", "burned", "confused"):
        v += 0.15
    return v

