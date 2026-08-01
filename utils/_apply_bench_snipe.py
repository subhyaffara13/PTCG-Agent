
def _apply_bench_snipe(gs, bench_damage):
    if bench_damage <= 0:
        return
    opp_bench = gs.get("opponent_bench", [])
    if isinstance(opp_bench, list):
        surviving_bench = []
        for bp in opp_bench:
            if isinstance(bp, dict):
                bp_hp = bp.get("hp", 100) - bench_damage
                if bp_hp > 0:
                    bp["hp"] = bp_hp
                    surviving_bench.append(bp)
        gs["opponent_bench"] = surviving_bench


def _apply_bench_snipe(gs, bench_damage):
    if bench_damage <= 0:
        return
    opp_bench = gs.get("opponent_bench", [])
    if isinstance(opp_bench, list):
        surviving_bench = []
        for bp in opp_bench:
            if isinstance(bp, dict):
                bp_hp = bp.get("hp", 100) - bench_damage
                if bp_hp > 0:
                    bp["hp"] = bp_hp
                    surviving_bench.append(bp)
        gs["opponent_bench"] = surviving_bench

