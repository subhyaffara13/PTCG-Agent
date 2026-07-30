from . import _registry, logger

def _score_attach_energy(v: float, action: str, gs: dict, ac: dict, bn: list, ahp: int) -> float:
    if not action.startswith("attach_energy:"):
        return v
    v += 0.45
    parts = action.split(":")
    target_id = parts[2] if len(parts) > 2 else ""
    active_id = str(ac.get("id", "")) if isinstance(ac, dict) else ""
    is_to_active = not target_id or target_id == active_id
    if is_to_active:
        if isinstance(ac, dict):
            need = 2
            try:
                e = _registry.get_full_skill(ac.get("id"))
                if e and e.energy_cost > 0:
                    need = e.energy_cost
            except Exception as e:
                logger.debug(f"Active pokemon energy cost check error: {e}")
            att = len(ac.get("attached", []) or ac.get("energies", []))
            if att < need:
                v += 0.35
                if att == need - 1:
                    v += 0.2
            elif att >= need:
                an = ac.get("card_name", "").lower()
                sc = any(sa in an for sa in {"raging bolt", "iron hands", "chien pao", "ceruledge", "garchomp", "roaring moon", "groudon", "kyogre"})
                nr = ahp <= 50 or gs.get("my_active_status", "") in {"poisoned", "burned", "asleep", "paralyzed"}
                if not sc and not nr:
                    v -= 0.25
    else:
        v += 0.1
        if len(parts) > 2:
            try:
                poke_id = parts[2]
                for bp in bn:
                    if isinstance(bp, dict) and str(bp.get("id", "")) == poke_id:
                        bench_att = len(bp.get("attached", []) or bp.get("energies", []))
                        bp_card = _registry.get_full_skill(poke_id)
                        if bp_card and bp_card.energy_cost > 0:
                            if bench_att < bp_card.energy_cost:
                                v += 0.2
                                if bench_att == bp_card.energy_cost - 1:
                                    v += 0.2
                            else:
                                v -= 0.3
                        break
            except Exception:
                pass
    return v
