from . import _CARD_NAME_TO_ID, _registry

def _score_learned(v: float, action: str, gs: dict) -> float:
    try:
        cid = None
        if action.startswith("bench:"):
            parts = action.split(":")
            if len(parts) > 1 and parts[1].lstrip("-").isdigit():
                cid = int(parts[1])
        elif action.startswith("evolve:"):
            parts = action.split(":")
            if len(parts) > 2 and parts[2].lstrip("-").isdigit():
                cid = int(parts[2])
        elif action.startswith("play_trainer:"):
            tn = action.split(":", 1)[1].lower()
            cid = _CARD_NAME_TO_ID.get(tn)
        if cid is not None:
            dos = getattr(_registry, "learned_dos", set())
            donts = getattr(_registry, "learned_donts", set())
            if cid in dos:
                v += 0.5
            if cid in donts:
                v -= 0.5
        turn = gs.get("turn_number", 1)
        bench_size = len(gs.get("my_bench", [])) if isinstance(gs.get("my_bench"), list) else 0
        target_setup = getattr(_registry, "target_setup_duration", None)
        if target_setup and target_setup <= 3 and turn <= 3:
            if action.startswith("attach_energy:"):
                v += 0.3
            elif action.startswith("attack:") and turn >= 2:
                v += 0.4
        target_bench = getattr(_registry, "target_bench_density", None)
        if target_bench and bench_size < target_bench and turn <= 5:
            if action.startswith("bench:"):
                v += 0.3
            elif action.startswith("play_trainer:"):
                tn = action.split(":", 1)[1].lower() if ":" in action else ""
                if any(k in tn for k in {"poffin", "nest ball", "ball", "ultra"}):
                    v += 0.25
        for rule in getattr(_registry, "behavior_donts_rules", []):
            if isinstance(rule, dict):
                cond = rule.get("condition", "")
                if cond == "setup_duration_gt_15" and turn > 12 and action == "pass":
                    v -= 0.5
                elif cond == "high_aggro_low_accel" and action.startswith("attack:"):
                    ac = gs.get("my_active_pokemon", {})
                    attached = len(ac.get("attached", []) or ac.get("energies", [])) if isinstance(ac, dict) else 0
                    if attached < 2:
                        v -= 0.3
    except Exception:
        pass
    return v
