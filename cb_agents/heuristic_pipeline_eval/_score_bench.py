from . import CardStage, _get_prize_yield, _registry

def _score_bench(v: float, action: str, gs: dict, bn: list, ac: dict) -> float:
    if not action.startswith("bench:"):
        return v
    if not bn:
        v += 0.8
    else:
        bs = len(bn)
        if bs < 2:
            v += 0.4
        elif bs < 3:
            v += 0.25
        elif bs < 4:
            v += 0.15
        else:
            v += 0.05
        pr = gs.get("priority_profile", "aggro_push")
        tol = {"aggro_push": 0.15, "closing": 0.10, "disruption": -0.05, "setup": 0.15, "stall": -0.15}.get(pr, 0.0)
        if bs >= 4 and tol < 0:
            v += tol * bs * 0.3
        elif bs >= 5 and tol <= 0:
            v -= 0.4
    try:
        bench_parts = action.split(":")
        bench_card_id = int(bench_parts[1]) if len(bench_parts) > 1 and bench_parts[1].isdigit() else None
        if bench_card_id is not None:
            bc = _registry.get_full_skill(bench_card_id)
            if bc:
                if bc.stage in (CardStage.STAGE1, CardStage.STAGE2):
                    v += 0.2
                if bc.hp and bc.hp > 120:
                    v += 0.1
                py = _get_prize_yield(bc.card_name)
                if py >= 2:
                    high_prize_count = 1 if _get_prize_yield(str(ac.get("card_name", "") if isinstance(ac, dict) else "")) >= 2 else 0
                    for bp in bn:
                        if isinstance(bp, dict):
                            hp_name = bp.get("card_name", "")
                            if _get_prize_yield(str(hp_name)) >= 2:
                                high_prize_count += 1
                    if high_prize_count >= 1:
                        penalty = 0.3 * py
                        boss_prob = gs.get("boss_prob", 0.0)
                        if boss_prob > 0.3:
                            penalty *= min(3.0, 1.0 + boss_prob * 2.0)
                        v -= penalty
    except Exception:
        pass
    return v
