from . import Any

def _handle_ko_and_prizes(gs, hand, CardRegistry):
    prize_yield = 1
    opp_active = gs.get("opponent_active", {})
    opp_id = gs.get("opponent_active_id") or (opp_active.get("id") if isinstance(opp_active, dict) else None)
    if opp_id is not None:
        try:
            c = CardRegistry().get(opp_id)
            if c is not None:
                n = c.card_name.lower()
                if "vmax" in n: prize_yield = 3
                elif "vstar" in n or n.endswith(" v") or n.endswith(" ex") or " ex " in n or " v " in n:
                    prize_yield = 2
        except Exception: pass
    gs["my_prizes"] = max(0, gs.get("my_prizes", 6) - prize_yield)
    gs["my_hand"] = hand + [0] * prize_yield
    opp_bench = list(gs.get("opponent_bench", []))
    if opp_bench:
        opp_promoted = opp_bench.pop(0)
        gs["opponent_active_hp"] = opp_promoted.get("hp", 100)
        gs["opponent_active_id"] = opp_promoted.get("id", None)
        gs["opponent_active"] = opp_promoted
        gs["opponent_bench"] = opp_bench
    else:
        gs["opponent_active_hp"] = 0
