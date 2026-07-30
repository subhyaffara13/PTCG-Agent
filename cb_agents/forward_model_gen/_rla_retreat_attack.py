from . import CardRegistry

def _rla_add_retreat_attack(gs, actions):
    bench = gs.get("my_bench", [])
    if isinstance(bench, list) and len(bench) > 0:
        for i in range(len(bench)):
            actions.append(f"retreat:{i}")
    opp_hp = gs.get("opponent_active_hp", 100)
    if opp_hp is not None and opp_hp > 0:
        my_active = gs.get("my_active_pokemon")
        can_attack = False
        if isinstance(my_active, dict):
            attached_count = len(my_active.get("attached", []))
            active_id = my_active.get("id")
            if active_id is not None and CardRegistry is not None:
                try:
                    min_cost = CardRegistry().get_min_energy_cost(active_id)
                    can_attack = attached_count >= min_cost
                except Exception:
                    can_attack = attached_count >= 1
            else: can_attack = attached_count >= 1
        else: can_attack = True
        if can_attack:
            actions.append("attack:strike")
