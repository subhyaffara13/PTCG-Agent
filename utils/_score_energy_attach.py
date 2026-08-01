
def _score_energy_attach(score, opt, card, registry, sel_type, select, current, my_idx):
    if sel_type not in (1, 4) and str(select.get("context", "")).lower() not in ("energy", "attach"):
        return score
    try:
        area = opt.get("area"); index = opt.get("index")
        p_idx = opt.get("playerIndex", 0)
        if current is None or p_idx != my_idx: return score
        players = current.get("players", [])
        my_state = players[my_idx]
        from ._resolve_opt_card import _resolve_instance
        instance = None
        if area == 4:
            instance = _resolve_instance(my_state.get("active"))
        elif area == 12:
            bench = my_state.get("bench", [])
            if len(bench) > index:
                instance = _resolve_instance(bench[index])
        if not instance: return score
        attached = instance.get("attached", [])
        attached_count = len(attached) if isinstance(attached, list) else 0
        required = getattr(card, "energy_cost", 0)
        if attached_count >= required: return score
        target_name = ""
        target_id = instance.get("id") if isinstance(instance, dict) else getattr(instance, "id", None)
        if target_id is not None and registry:
            target_card = registry.get_full_skill(target_id)
            if target_card:
                target_name = getattr(target_card, "card_name", "").lower()
        is_passive = any(s in target_name for s in {"dunsparce", "bidoof", "snom", "remoraid", "jirachi", "manaphy"})
        target_hp = instance.get("hp", 100) if isinstance(instance, dict) else getattr(instance, "hp", 100)
        target_max_hp = instance.get("maxHp", 100) if isinstance(instance, dict) else getattr(instance, "maxHp", 100)
        is_low_hp = target_hp <= 40 and target_max_hp <= 130
        if is_passive or is_low_hp:
            boost = -15.0
        else:
            boost = 10.0 * (required - attached_count)
            if area == 4: boost += 5.0
        score += boost
    except Exception: pass
    return score

