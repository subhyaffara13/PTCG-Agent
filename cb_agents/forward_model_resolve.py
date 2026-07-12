from typing import Any

from cb_agents.forward_model_gen import _remove_from_hand, _int_or_str, _apply_evolve, _draw_cards, _ABILITY_DRAW
from cb_agents.card_registry import CardRegistry


def _resolve_base(gs: dict, hand: list, action: str) -> None:
    parts = action.split(":", 1)
    act_type = parts[0]
    target = parts[1] if len(parts) > 1 else ""

    if act_type == "pass":
        gs["turn_ended"] = True

    elif act_type == "bench":
        _remove_from_hand(hand, _int_or_str(target))
        gs["my_hand"] = hand
        bench = list(gs.get("my_bench", []))
        poke_hp = 100
        try:
            c = CardRegistry().get_full_skill(_int_or_str(target))
            if c and c.hp:
                poke_hp = c.hp
        except Exception:
            pass
        bench.append({"id": _int_or_str(target), "hp": poke_hp, "attached": []})
        gs["my_bench"] = bench

    elif act_type == "evolve":
        _apply_evolve(gs, _int_or_str(target))

    elif act_type == "attach_energy":
        card_target = target.split(":", 1)
        card_id = card_target[0]
        poke_id = card_target[1] if len(card_target) > 1 else None
        
        _remove_from_hand(hand, _int_or_str(card_id))
        gs["my_hand"] = hand
        
        valid_targets = []
        if isinstance(gs.get("my_active_pokemon"), dict):
            valid_targets.append(gs["my_active_pokemon"])
        bench = gs.get("my_bench", [])
        if isinstance(bench, list):
            valid_targets.extend([p for p in bench if isinstance(p, dict)])
            
        if valid_targets:
            chosen = None
            if poke_id:
                for p in valid_targets:
                    if str(p.get("id")) == poke_id:
                        chosen = p
                        break
            if not chosen:
                best_target = None
                best_need = -1
                active_poke = gs.get("my_active_pokemon")
                active_id = active_poke.get("id") if isinstance(active_poke, dict) else None
                for p in valid_targets:
                    att_count = len(p.get("attached", []))
                    poke_id = p.get("id")
                    need = 3
                    try:
                        if poke_id is not None:
                            pc = CardRegistry().get_full_skill(poke_id)
                            if pc and pc.energy_cost > 0:
                                need = pc.energy_cost
                    except Exception:
                        pass
                    deficit = max(0, need - att_count)
                    is_active = (active_id is not None and p.get("id") == active_id)
                    score = deficit + (0.5 if is_active else 0.0)
                    if score > best_need:
                        best_need = score
                        best_target = p
                chosen = best_target or valid_targets[0]
            attached = list(chosen.get("attached", []))
            attached.append(card_id)
            chosen["attached"] = attached

    elif act_type == "retreat":
        from cb_agents.forward_model_resolve_helpers import handle_retreat_helper
        handle_retreat_helper(gs, target, CardRegistry)

    elif act_type == "attack":
        from cb_agents.forward_model_resolve_helpers import handle_attack_helper
        handle_attack_helper(gs, hand, CardRegistry)

    elif act_type == "play_trainer":
        from cb_agents.forward_model_resolve_helpers import handle_play_trainer_helper
        handle_play_trainer_helper(gs, hand, target, CardRegistry, _int_or_str, _remove_from_hand, _draw_cards)

    elif act_type == "ability":
        name = target.lower() if target else ""
        if any(k in name for k in _ABILITY_DRAW):
            gs["my_hand"] = _draw_cards(hand, gs, 3)

    elif act_type == "take_prize":
        my_prizes = gs.get("my_prizes", [])
        if isinstance(my_prizes, list) and my_prizes:
            idx = int(target) if target.isdigit() else 0
            if 0 <= idx < len(my_prizes):
                taken = my_prizes.pop(idx)
                hand.append(taken)
                gs["my_hand"] = hand
                gs["my_prizes"] = my_prizes
        prize_count = gs.get("prize_count", 1) - 1
        if prize_count <= 0:
            gs["select_prize"] = False
        else:
            gs["prize_count"] = prize_count
