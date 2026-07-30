from . import _registry

def _score_attach_energy_rank(action, game_state, active_attached, active):
    micro = 0
    parts = action.split(":")
    energy_card = parts[1] if len(parts) > 1 else ""
    target_id = parts[2] if len(parts) > 2 else (parts[1] if len(parts) == 2 else "")
    try:
        from cb_agents.preference_maps import get_energy_preference
        preferred_energy = get_energy_preference(target_id)
        if target_id and preferred_energy and preferred_energy != energy_card:
            micro = 25
    except ImportError:
        pass
    is_active_target = False
    if target_id:
        target_id_str = target_id.lower()
        active_id = str(active.get("id", "")).lower()
        if target_id_str in ("active", "my_active_pokemon") or (active_id and target_id_str == active_id):
            is_active_target = True
    if is_active_target:
        needed = 3
        try:
            if isinstance(active, dict):
                active_card_id = active.get("id")
                if active_card_id is not None:
                    c = _registry.get_full_skill(active_card_id)
                    if c and c.energy_cost > 0:
                        needed = c.energy_cost
        except Exception:
            pass
        hp = game_state.get("my_active_hp", 100)
        if hp <= 50 or active_attached >= needed:
            micro += 40
        elif active_attached == 0:
            micro -= 2
        else:
            micro -= 1
    else:
        bench_penalty = -3
        try:
            poke_id = target_id
            for bp in game_state.get("my_bench", []):
                if isinstance(bp, dict) and str(bp.get("id", "")) == poke_id:
                    bench_att = len(bp.get("attached", []) or bp.get("energies", []))
                    bp_card = _registry.get_full_skill(poke_id)
                    if bp_card and bp_card.energy_cost > 0 and bench_att >= bp_card.energy_cost:
                        bench_penalty = 15
                    break
        except Exception:
            pass
        micro += bench_penalty
    return micro
