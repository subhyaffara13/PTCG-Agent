import random

def _handle_energy_utils(gs, hand, base_name, CardRegistry, int_or_str, draw_cards):
    if any(k in base_name for k in {"energy search", "energy-search"}):
        if gs.get("my_decklist"):
            energy_ids = [k for k, v in gs["my_decklist"].items()
                          if str(v.get("card_type", "")).startswith("ENERGY") or str(v.get("type", "")).upper() in ("ENERGY",)]
            if not energy_ids:
                energy_ids = [eid for eid in list(gs["my_decklist"].keys()) if str(eid).isdigit() and int(eid) in (4, 6)]
            if energy_ids:
                gs["my_hand"] = hand + [random.choice(energy_ids)]
                gs["my_deck_count"] = gs.get("my_deck_count", 60) - 1
        return True
    if any(k in base_name for k in {"energy switch", "energy-switch"}):
        valid_pokemon = []
        if isinstance(gs.get("my_active_pokemon"), dict) and gs["my_active_pokemon"].get("attached"):
            valid_pokemon.append(gs["my_active_pokemon"])
        bench = gs.get("my_bench", [])
        if isinstance(bench, list):
            for p in bench:
                if isinstance(p, dict) and p.get("attached"):
                    valid_pokemon.append(p)
        if len(valid_pokemon) >= 2:
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
        return True
    if any(k in base_name for k in {"energy retrieval", "energy-retrieval"}):
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
        return True
    if any(k in base_name for k in {"enhanced hammer", "enhanced-hammer"}):
        opp_active = gs.get("opponent_active_pokemon", {})
        if isinstance(opp_active, dict) and opp_active.get("attached"):
            opp_attached = list(opp_active["attached"])
            specials = [cid for cid in opp_attached if str(cid) not in ("4", "6")]
            if specials:
                removed = specials[0] if len(specials) == 1 else random.choice(specials)
                opp_attached.remove(removed)
                opp_active["attached"] = opp_attached
                gs["opponent_active_pokemon"] = opp_active
        return True
    return False
