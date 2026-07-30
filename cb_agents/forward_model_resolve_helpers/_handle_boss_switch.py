import random

def _handle_boss_switch(gs, base_name):
    if any(k in base_name for k in {"boss", "orders"}):
        opp_bench = gs.get("opponent_bench", [])
        if isinstance(opp_bench, list) and opp_bench:
            gusted = random.choice(opp_bench)
            if isinstance(gusted, dict):
                old_opponent_active = gs.get("opponent_active_pokemon", {})
                new_active = gusted.copy()
                opp_bench = [p for p in opp_bench if p is not gusted]
                if old_opponent_active:
                    opp_bench.append(old_opponent_active)
                gs["opponent_bench"] = opp_bench
                gs["opponent_active_pokemon"] = new_active
                gs["opponent_active_hp"] = new_active.get("hp", gs.get("opponent_active_hp", 100))
        return True
    if any(k in base_name for k in {"switch"}):
        bench = list(gs.get("my_bench", []))
        if bench:
            new_active = random.choice(bench)
            bench = [p for p in bench if p is not new_active]
            old_active = gs.get("my_active_pokemon", {})
            if old_active:
                bench.append(old_active)
            gs["my_bench"] = bench
            gs["my_active_pokemon"] = new_active
        return True
    return False
