from typing import Any

def apply_evolve_helper(gs: dict, card_id: Any, CardRegistry: Any, remove_from_hand: Any) -> None:
    hand = list(gs.get("my_hand", []))
    remove_from_hand(hand, card_id)
    gs["my_hand"] = hand

    prev_stage_id = None
    if CardRegistry is not None:
        try:
            c = CardRegistry().get(int(card_id) if not isinstance(card_id, int) else card_id)
            if c and c.previous_stage:
                prev_stage_id = c.previous_stage
        except Exception:
            pass

    evolved_hp = 150
    if CardRegistry is not None:
        try:
            c = CardRegistry().get_full_skill(card_id)
            if c and c.hp:
                evolved_hp = c.hp
        except Exception:
            pass

    search_id = prev_stage_id if prev_stage_id is not None else card_id
    bench = list(gs.get("my_bench", []))
    for i, poke in enumerate(bench):
        if isinstance(poke, dict) and str(poke.get("id")) == str(search_id):
            bench[i] = {"id": f"evolved_{card_id}", "hp": evolved_hp, "attached": list(poke.get("attached", []))}
            gs["my_bench"] = bench
            return
    active = gs.get("my_active_pokemon", {})
    if isinstance(active, dict) and str(active.get("id")) == str(search_id):
        gs["my_active_pokemon"] = {"id": f"evolved_{card_id}", "hp": evolved_hp, "attached": list(active.get("attached", []))}
