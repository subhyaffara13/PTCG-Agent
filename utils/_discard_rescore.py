
def _discard_rescore(scored_options, options, registry, observation):
    try:
        current = observation.get("current", {})
        my_idx = current.get("yourIndex", 0)
        players = current.get("players", [])
        my_state = players[my_idx] if len(players) > my_idx else {}
        bench_slots = len(my_state.get("bench", []))
        active_poke = my_state.get("active", None)
        has_active = bool(active_poke and len(active_poke) > 0 and active_poke[0])
        my_hand = my_state.get("hand", [])
        hand_ids = [c.get("id") for c in my_hand if c]
        for i in range(len(scored_options)):
            idx, base_score = scored_options[i]
            opt = options[idx]
            cid = opt.get("id")
            if cid is None:
                area = opt.get("area")
                idx2 = opt.get("index")
                if area == 2 and len(my_hand) > idx2:
                    cid = my_hand[idx2].get("id")
            if cid is None:
                continue
            card = registry.get_full_skill(cid)
            if not card:
                continue
            ct = getattr(card, "card_type", None)
            ct_name = ct.name if ct else ""
            card_id_int = int(cid) if not isinstance(cid, int) else cid
            if ct_name == "POKEMON":
                count_in_hand = sum(1 for hid in hand_ids if str(hid) == str(cid))
                is_last_copy = count_in_hand <= 1
                bench_needed = (6 - bench_slots) if has_active else (6 - bench_slots - 1)
                if bench_needed > 0 and is_last_copy:
                    base_score += 25.0
                elif bench_needed > 0:
                    base_score += 10.0
            elif ct_name == "ENERGY":
                total_on_board = 0
                if active_poke and len(active_poke) > 0:
                    total_on_board += len(active_poke[0].get("attached", []))
                for b in my_state.get("bench", []):
                    if b and len(b) > 0:
                        total_on_board += len(b[0].get("attached", []))
                if total_on_board >= 8:
                    base_score -= 8.0
                elif total_on_board >= 5:
                    base_score -= 3.0
            elif ct_name == "TRAINER":
                if card_id_int in registry.learned_dos:
                    base_score -= 6.0
            scored_options[i] = (idx, base_score)
    except Exception:
        pass
    return scored_options

