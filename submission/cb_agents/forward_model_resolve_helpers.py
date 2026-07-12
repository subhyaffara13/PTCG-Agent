import logging
logger = logging.getLogger(__name__)
from typing import Any

def handle_retreat_helper(gs: dict, target: str, CardRegistry: Any) -> None:
    bench = list(gs.get("my_bench", []))
    if bench:
        old_active = gs.get("my_active_pokemon", {})
        target_idx = None
        if target:
            try:
                target_idx = int(target)
            except ValueError:
                for i, p in enumerate(bench):
                    if isinstance(p, dict) and str(p.get("id")) == target:
                        target_idx = i
                        break
        if target_idx is None or target_idx < 0 or target_idx >= len(bench):
            target_idx = 0
        new_active = bench.pop(target_idx)
        
        retreat_cost = 1
        try:
            card = CardRegistry().get_full_skill(old_active.get("id"))
            if card is not None:
                retreat_cost = card.retreat_cost
        except Exception as e:
            logger.error(f"Failed to retrieve card retreat cost: {e}")
            
        attached = list(old_active.get("attached", []))
        removed_energies = []
        for _ in range(min(retreat_cost, len(attached))):
            removed_energies.append(attached.pop(0))
        old_active["attached"] = attached
        gs["my_discard"] = gs.get("my_discard", []) + removed_energies
        
        bench.append(old_active)
        gs["my_bench"] = bench
        gs["my_active_pokemon"] = new_active

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

def handle_play_trainer_helper(gs: dict, hand: list, target: str, CardRegistry: Any, int_or_str: Any, remove_from_hand: Any, draw_cards: Any) -> None:
    name = target.lower() if target else ""
    base_name = name.replace("_tails", "").replace("_heads", "")

    removed = False
    if CardRegistry is not None:
        for i, card_id in enumerate(list(hand)):
            try:
                c = CardRegistry().get(int_or_str(card_id))
                if c and c.card_name.lower() == base_name:
                    hand.pop(i)
                    removed = True
                    break
            except Exception:
                pass
    if not removed:
        remove_from_hand(hand, target)
    
    gs["my_hand"] = hand

    if name.endswith("_tails"):
        return

    if any(k in base_name for k in {"research", "professor"}):
        gs["my_discard"] = gs.get("my_discard", []) + hand.copy()
        hand.clear()
        gs["my_hand"] = draw_cards(hand, gs, 7)
    elif any(k in base_name for k in {"iono", "judge"}):
        gs["my_deck"] = gs.get("my_deck", []) + hand.copy()
        gs["my_deck_count"] = gs.get("my_deck_count", 60) + len(hand)
        hand.clear()
        gs["my_hand"] = draw_cards(hand, gs, 4)
    # Dusk Ball: look at bottom 7, get a Pokemon (check BEFORE generic ball handler)
    elif "dusk" in base_name and any(k in base_name for k in {"ball"}):
        if gs.get("my_decklist"):
            import random
            pokemon_ids = [k for k, v in gs["my_decklist"].items() if str(v.get("card_type", "")).startswith("POKEMON")]
            if pokemon_ids:
                gs["my_hand"] = hand + [random.choice(pokemon_ids)]
                gs["my_deck_count"] = gs.get("my_deck_count", 60) - 1
    # Ultra Ball: discard 2, search Pokemon
    elif "ultra" in base_name and any(k in base_name for k in {"ball"}):
        discards = []
        for _ in range(min(2, len(hand))):
            discards.append(hand.pop(0))
        gs["my_discard"] = gs.get("my_discard", []) + discards
        added = 1
        if gs.get("my_deck"):
            import random
            added = random.choice(gs["my_deck"])
        elif gs.get("my_decklist"):
            import random
            added = random.choice(list(gs["my_decklist"].keys()))
        gs["my_hand"] = hand + [added]
        gs["my_deck_count"] = gs.get("my_deck_count", 60) - 1
    # Other ball search cards
    elif any(k in base_name for k in {"ball"}):
        added = 1
        if gs.get("my_deck"):
            import random
            added = random.choice(gs["my_deck"])
        elif gs.get("my_decklist"):
            import random
            added = random.choice(list(gs["my_decklist"].keys()))
        gs["my_hand"] = hand + [added]
        gs["my_deck_count"] = gs.get("my_deck_count", 60) - 1
    elif "secret box" in base_name or "petrel" in base_name:
        added1, added2 = 1, 2
        if gs.get("my_deck"):
            import random
            added1 = random.choice(gs["my_deck"])
            added2 = random.choice(gs["my_deck"])
        elif gs.get("my_decklist"):
            import random
            keys = list(gs["my_decklist"].keys())
            added1 = random.choice(keys)
            added2 = random.choice(keys)
        gs["my_hand"] = hand + [added1, added2]
        gs["my_deck_count"] = gs.get("my_deck_count", 60) - 2
    
    # Boss's Orders: swap opponent active with a benched Pokemon
    elif any(k in base_name for k in {"boss", "orders"}):
        
    # Boss's Orders: swap opponent active with a benched Pokemon
    elif any(k in base_name for k in {"boss", "orders"}):
        opp_bench = gs.get("opponent_bench", [])
        if isinstance(opp_bench, list) and opp_bench:
            import random
            gusted = random.choice(opp_bench)
            new_active = gusted
            if isinstance(gusted, dict):
                old_opponent_active = gs.get("opponent_active_pokemon", {})
                new_active = gusted.copy()
                opp_bench = [p for p in opp_bench if p is not gusted]
                if old_opponent_active:
                    opp_bench.append(old_opponent_active)
                gs["opponent_bench"] = opp_bench
                gs["opponent_active_pokemon"] = new_active
                gs["opponent_active_hp"] = new_active.get("hp", gs.get("opponent_active_hp", 100))
    
    # Switch: swap our active with a benched Pokemon (free retreat, no energy discard)
    elif any(k in base_name for k in {"switch"}):
        bench = list(gs.get("my_bench", []))
        if bench:
            import random
            new_active = random.choice(bench)
            bench = [p for p in bench if p is not new_active]
            old_active = gs.get("my_active_pokemon", {})
            if old_active:
                bench.append(old_active)
            gs["my_bench"] = bench
            gs["my_active_pokemon"] = new_active
    
    # Larry's Skill / draw-to-hand-size effects
    elif any(k in base_name for k in {"larry", "skill"}) and "secret" not in base_name:
        target_count = 3
        if "3" in base_name:
            target_count = 3
        current_hand = len(gs.get("my_hand", []))
        if current_hand < target_count:
            gs["my_hand"] = draw_cards(hand, gs, target_count - current_hand)
    
    # Energy Search: search deck for basic energy
    elif any(k in base_name for k in {"energy search", "energy-search"}):
        if gs.get("my_decklist"):
            import random
            energy_ids = [k for k, v in gs["my_decklist"].items() if str(v.get("card_type", "")).startswith("ENERGY") or str(v.get("type", "")).upper() in ("ENERGY",)]
            if not energy_ids:
                energy_ids = [eid for eid in list(gs["my_decklist"].keys()) if str(eid).isdigit() and int(eid) in (4, 6)]
            if energy_ids:
                gs["my_hand"] = hand + [random.choice(energy_ids)]
                gs["my_deck_count"] = gs.get("my_deck_count", 60) - 1
    
    # Energy Switch: move energy from one Pokemon to another
    elif any(k in base_name for k in {"energy switch", "energy-switch"}):
        valid_pokemon = []
        if isinstance(gs.get("my_active_pokemon"), dict) and gs["my_active_pokemon"].get("attached"):
            valid_pokemon.append(gs["my_active_pokemon"])
        bench = gs.get("my_bench", [])
        if isinstance(bench, list):
            for p in bench:
                if isinstance(p, dict) and p.get("attached"):
                    valid_pokemon.append(p)
        if len(valid_pokemon) >= 2:
            import random
            donor = random.choice(valid_pokemon)
            remaining = [p for p in valid_pokemon if p is not donor]
            recipient = random.choice(remaining)
            donor_attached = list(donor.get("attached", []))
            if donor_attached:
                moved = donor_attached.pop(0)
                donor["attached"] = donor_attached
                recipient_attached = list(recipient.get("attached", []))
                recipient_attached.append(moved)
                recipient["attached"] = recipient_attached
    
    # Energy Retrieval: get 2 basic energy from discard to hand
    elif any(k in base_name for k in {"energy retrieval", "energy-retrieval"}):
        my_discard = gs.get("my_discard", [])
        if my_discard:
            energy_in_discard = []
            for cid in my_discard:
                try:
                    c = CardRegistry().get(int_or_str(cid))
                    if c and getattr(c.card_type, "name", "") == "ENERGY":
                        energy_in_discard.append(cid)
                except Exception:
                    if str(cid).isdigit() and int(cid) in (4, 6):
                        energy_in_discard.append(cid)
            taken = energy_in_discard[:2]
            for cid in taken:
                try:
                    my_discard.remove(cid)
                except ValueError:
                    pass
            gs["my_discard"] = my_discard
            gs["my_hand"] = hand + taken
    
    # Enhanced Hammer: discard opponent's special energy
    elif any(k in base_name for k in {"enhanced hammer", "enhanced-hammer"}):
        opp_active = gs.get("opponent_active_pokemon", {})
        if isinstance(opp_active, dict) and opp_active.get("attached"):
            opp_attached = list(opp_active["attached"])
            has_special = any(
                str(cid) not in ("4", "6")  # not basic {L} or {F}
                for cid in opp_attached
            )
            if has_special:
                import random
                specials = [cid for cid in opp_attached if str(cid) not in ("4", "6")]
                removed = specials[0] if len(specials) == 1 else random.choice(specials)
                opp_attached.remove(removed)
                opp_active["attached"] = opp_attached
                gs["opponent_active_pokemon"] = opp_active
    
    # Night Stretcher: put Pokemon from discard to hand
    elif any(k in base_name for k in {"night stretcher", "night-stretcher"}):
        my_discard = gs.get("my_discard", [])
        if my_discard:
            pokemon_in_discard = []
            for cid in my_discard:
                try:
                    c = CardRegistry().get(int_or_str(cid))
                    if c and getattr(c.card_type, "name", "") == "POKEMON":
                        pokemon_in_discard.append(cid)
                except Exception:
                    pass
            if pokemon_in_discard:
                import random
                recovered = random.choice(pokemon_in_discard)
                try:
                    my_discard.remove(recovered)
                except ValueError:
                    pass
                gs["my_discard"] = my_discard
                gs["my_hand"] = hand + [recovered]
    
    # Pokegear 3.0: look at top 7 cards, add a Trainer to hand
    elif any(k in base_name for k in {"pokegear", "poke-gear"}):
        if gs.get("my_decklist"):
            import random
            trainer_ids = [k for k, v in gs["my_decklist"].items() if str(v.get("card_type", "")).startswith("TRAINER")]
            if trainer_ids:
                gs["my_hand"] = hand + [random.choice(trainer_ids)]
                gs["my_deck_count"] = gs.get("my_deck_count", 60) - 1
    

