from typing import Any

def handle_attack_helper(gs: dict, hand: list, CardRegistry: Any) -> None:
    try:
        actual_damage = int(gs.get("my_active_damage", 0))
    except (ValueError, TypeError):
        actual_damage = 0
        
    my_active = gs.get("my_active_pokemon", {})
    my_active_id = my_active.get("id") if isinstance(my_active, dict) else my_active
    my_active_name = None
    if not actual_damage and my_active_id is not None and CardRegistry is not None:
        try:
            registry = CardRegistry()
            attached_count = len(my_active.get("attached", [])) if isinstance(my_active, dict) else 0
            actual_damage, my_active_name = registry.get_best_attack_damage_with_name(my_active_id, attached_count)
        except Exception:
            pass
    if not actual_damage:
        try:
            if CardRegistry is not None and my_active_id is not None:
                card = CardRegistry().get_full_skill(my_active_id)
                if card is not None:
                    actual_damage = int(card.damage_output)
                    my_active_name = card.card_name
        except Exception:
            pass

    # Apply status conditions based on attack name
    _apply_status_to_opponent(gs, my_active_name or "")
            
    try:
        opp_hp = int(gs.get("opponent_active_hp", 100))
    except (ValueError, TypeError):
        opp_hp = 100
        
    # Apply weakness (2x) and resistance (-30) if we can determine types
    if actual_damage > 0 and CardRegistry is not None:
        try:
            registry = CardRegistry()
            if my_active_id is not None:
                atk_type = registry.card_poke_type.get(int(my_active_id) if not isinstance(my_active_id, int) else my_active_id, "")
            else:
                atk_type = ""
            opp_active = gs.get("opponent_active", {})
            opp_id = gs.get("opponent_active_id") or (opp_active.get("id") if isinstance(opp_active, dict) else None)
            if opp_id is not None:
                opp_id_int = int(opp_id) if not isinstance(opp_id, int) else opp_id
                opp_weakness = registry.card_weakness.get(opp_id_int, "")
                opp_resistance = registry.card_resistance.get(opp_id_int, "")
                if atk_type and opp_weakness and atk_type == opp_weakness:
                    actual_damage *= 2
                if atk_type and opp_resistance and atk_type == opp_resistance:
                    actual_damage = max(0, actual_damage - 30)
        except Exception:
            pass
        
    # Check for bench snipe damage (attacks with "snipe" or "spread" in action name)
    bench_damage = gs.get("my_active_bench_damage", 0)
    if bench_damage > 0:
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
        
    gs["opponent_active_hp"] = max(0, opp_hp - actual_damage)
    if gs["opponent_active_hp"] <= 0:
        prize_yield = 1
        opp_active = gs.get("opponent_active", {})
        opp_id = gs.get("opponent_active_id") or (opp_active.get("id") if isinstance(opp_active, dict) else None)
        if opp_id is not None:
            try:
                c = CardRegistry().get(opp_id)
                if c is not None:
                    n = c.card_name.lower()
                    if "vmax" in n: prize_yield = 3
                    elif "vstar" in n or n.endswith(" v") or n.endswith(" ex") or " ex " in n or " v " in n: prize_yield = 2
            except Exception:
                pass
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
    # Clear active status after attack turn ends
    gs["my_active_status"] = ""
    gs["turn_ended"] = True


def handle_attack_helper(gs: dict, hand: list, CardRegistry: Any) -> None:
    try:
        actual_damage = int(gs.get("my_active_damage", 0))
    except (ValueError, TypeError):
        actual_damage = 0
        
    my_active = gs.get("my_active_pokemon", {})
    my_active_id = my_active.get("id") if isinstance(my_active, dict) else my_active
    if not actual_damage and my_active_id is not None and CardRegistry is not None:
        try:
            registry = CardRegistry()
            attached_count = len(my_active.get("attached", [])) if isinstance(my_active, dict) else 0
            actual_damage = registry.get_best_attack_damage(my_active_id, attached_count)
        except Exception:
            pass
    if not actual_damage:
        try:
            if CardRegistry is not None and my_active_id is not None:
                card = CardRegistry().get_full_skill(my_active_id)
                if card is not None:
                    actual_damage = int(card.damage_output)
        except Exception:
            pass
            
    try:
        opp_hp = int(gs.get("opponent_active_hp", 100))
    except (ValueError, TypeError):
        opp_hp = 100
        
    if actual_damage > 0 and CardRegistry is not None:
        try:
            registry = CardRegistry()
            if my_active_id is not None:
                atk_type = registry.card_poke_type.get(int(my_active_id) if not isinstance(my_active_id, int) else my_active_id, "")
            else:
                atk_type = ""
            opp_active = gs.get("opponent_active", {})
            opp_id = gs.get("opponent_active_id") or (opp_active.get("id") if isinstance(opp_active, dict) else None)
            if opp_id is not None:
                opp_id_int = int(opp_id) if not isinstance(opp_id, int) else opp_id
                opp_weakness = registry.card_weakness.get(opp_id_int, "")
                opp_resistance = registry.card_resistance.get(opp_id_int, "")
                if atk_type and opp_weakness and atk_type == opp_weakness:
                    actual_damage *= 2
                if atk_type and opp_resistance and atk_type == opp_resistance:
                    actual_damage = max(0, actual_damage - 30)
        except Exception:
            pass
        
    gs["opponent_active_hp"] = max(0, opp_hp - actual_damage)
    if gs["opponent_active_hp"] <= 0:
        prize_yield = 1
        opp_active = gs.get("opponent_active", {})
        opp_id = gs.get("opponent_active_id") or (opp_active.get("id") if isinstance(opp_active, dict) else None)
        if opp_id is not None:
            try:
                c = CardRegistry().get(opp_id)
                if c is not None:
                    n = c.card_name.lower()
                    if "vmax" in n: prize_yield = 3
                    elif "vstar" in n or n.endswith(" v") or n.endswith(" ex") or " ex " in n or " v " in n: prize_yield = 2
            except Exception:
                pass
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
    gs["turn_ended"] = True


def handle_attack_helper(gs: dict, hand: list, CardRegistry: Any) -> None:
    try:
        actual_damage = int(gs.get("my_active_damage", 0))
    except (ValueError, TypeError):
        actual_damage = 0
        
    my_active = gs.get("my_active_pokemon", {})
    my_active_id = my_active.get("id") if isinstance(my_active, dict) else my_active
    my_active_name = None
    if not actual_damage and my_active_id is not None and CardRegistry is not None:
        try:
            registry = CardRegistry()
            attached_count = len(my_active.get("attached", [])) if isinstance(my_active, dict) else 0
            actual_damage, my_active_name = registry.get_best_attack_damage_with_name(my_active_id, attached_count)
        except Exception:
            pass
    if not actual_damage:
        try:
            if CardRegistry is not None and my_active_id is not None:
                card = CardRegistry().get_full_skill(my_active_id)
                if card is not None:
                    actual_damage = int(card.damage_output)
                    my_active_name = card.card_name
        except Exception:
            pass

    # Apply status conditions based on attack name
    _apply_status_to_opponent(gs, my_active_name or "")
            
    try:
        opp_hp = int(gs.get("opponent_active_hp", 100))
    except (ValueError, TypeError):
        opp_hp = 100
        
    # Apply weakness (2x) and resistance (-30) if we can determine types
    if actual_damage > 0 and CardRegistry is not None:
        try:
            registry = CardRegistry()
            if my_active_id is not None:
                atk_type = registry.card_poke_type.get(int(my_active_id) if not isinstance(my_active_id, int) else my_active_id, "")
            else:
                atk_type = ""
            opp_active = gs.get("opponent_active", {})
            opp_id = gs.get("opponent_active_id") or (opp_active.get("id") if isinstance(opp_active, dict) else None)
            if opp_id is not None:
                opp_id_int = int(opp_id) if not isinstance(opp_id, int) else opp_id
                opp_weakness = registry.card_weakness.get(opp_id_int, "")
                opp_resistance = registry.card_resistance.get(opp_id_int, "")
                if atk_type and opp_weakness and atk_type == opp_weakness:
                    actual_damage *= 2
                if atk_type and opp_resistance and atk_type == opp_resistance:
                    actual_damage = max(0, actual_damage - 30)
        except Exception:
            pass
        
    # Check for bench snipe damage (attacks with "snipe" or "spread" in action name)
    bench_damage = gs.get("my_active_bench_damage", 0)
    if bench_damage > 0:
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
        
    gs["opponent_active_hp"] = max(0, opp_hp - actual_damage)
    if gs["opponent_active_hp"] <= 0:
        prize_yield = 1
        opp_active = gs.get("opponent_active", {})
        opp_id = gs.get("opponent_active_id") or (opp_active.get("id") if isinstance(opp_active, dict) else None)
        if opp_id is not None:
            try:
                c = CardRegistry().get(opp_id)
                if c is not None:
                    n = c.card_name.lower()
                    if "vmax" in n: prize_yield = 3
                    elif "vstar" in n or n.endswith(" v") or n.endswith(" ex") or " ex " in n or " v " in n: prize_yield = 2
            except Exception:
                pass
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
    # Clear active status after attack turn ends
    gs["my_active_status"] = ""
    gs["turn_ended"] = True

