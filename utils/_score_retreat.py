
def _score_retreat(v: float, action: str, gs: dict, ahp: int) -> float:
    if not action.startswith("retreat:"):
        return v
    v += 0.4 if ahp <= 60 else -1.2
    try:
        target_idx = -1
        if ":" in action:
            target_str = action.split(":", 1)[1]
            if target_str.isdigit():
                target_idx = int(target_str)
        bench = gs.get("my_bench", [])
        if 0 <= target_idx < len(bench):
            target_poke = bench[target_idx]
            if isinstance(target_poke, dict):
                attached_list = target_poke.get("attached") or target_poke.get("energies") or []
                target_attached = len(attached_list)
                target_id = target_poke.get("id")
                if target_id is not None:
                    tc = _registry.get_full_skill(target_id)
                    is_better_attacker = tc and tc.damage_output > 0 and target_attached >= max(1, tc.energy_cost)
                    if is_better_attacker:
                        v += 0.8
                    elif target_attached == 0:
                        v -= 0.8
    except Exception as ex:
        logger.warning(f"Error parsing retreat target: {ex}")
    rsb = gs.get("retreat_score_boost", 0.0)
    if rsb > 0:
        v += rsb
    return v


def _score_retreat(v: float, action: str, gs: dict, ahp: int) -> float:
    if not action.startswith("retreat:"):
        return v
    v += 0.4 if ahp <= 60 else -1.2
    try:
        target_idx = -1
        if ":" in action:
            target_str = action.split(":", 1)[1]
            if target_str.isdigit():
                target_idx = int(target_str)
        bench = gs.get("my_bench", [])
        if 0 <= target_idx < len(bench):
            target_poke = bench[target_idx]
            if isinstance(target_poke, dict):
                attached_list = target_poke.get("attached") or target_poke.get("energies") or []
                target_attached = len(attached_list)
                target_id = target_poke.get("id")
                if target_id is not None:
                    tc = _registry.get_full_skill(target_id)
                    is_better_attacker = tc and tc.damage_output > 0 and target_attached >= max(1, tc.energy_cost)
                    if is_better_attacker:
                        v += 0.8
                    elif target_attached == 0:
                        v -= 0.8
    except Exception as ex:
        logger.warning(f"Error parsing retreat target: {ex}")
    rsb = gs.get("retreat_score_boost", 0.0)
    if rsb > 0:
        v += rsb
    return v

