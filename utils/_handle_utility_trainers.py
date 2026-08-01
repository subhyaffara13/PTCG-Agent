
def _handle_utility_trainers(gs, hand, base_name, CardRegistry, int_or_str):
    if any(k in base_name for k in {"night stretcher", "night-stretcher"}):
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
                recovered = random.choice(pokemon_in_discard)
                try:
                    my_discard.remove(recovered)
                except ValueError:
                    pass
                gs["my_discard"] = my_discard
                gs["my_hand"] = hand + [recovered]
        return True
    if any(k in base_name for k in {"pokegear", "poke-gear"}):
        if gs.get("my_decklist"):
            trainer_ids = [k for k, v in gs["my_decklist"].items()
                           if str(v.get("card_type", "")).startswith("TRAINER")]
            if trainer_ids:
                gs["my_hand"] = hand + [random.choice(trainer_ids)]
                gs["my_deck_count"] = gs.get("my_deck_count", 60) - 1
        return True
    return False


def _handle_utility_trainers(gs, hand, base_name, CardRegistry, int_or_str):
    if any(k in base_name for k in {"night stretcher", "night-stretcher"}):
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
                recovered = random.choice(pokemon_in_discard)
                try:
                    my_discard.remove(recovered)
                except ValueError:
                    pass
                gs["my_discard"] = my_discard
                gs["my_hand"] = hand + [recovered]
        return True
    if any(k in base_name for k in {"pokegear", "poke-gear"}):
        if gs.get("my_decklist"):
            trainer_ids = [k for k, v in gs["my_decklist"].items()
                           if str(v.get("card_type", "")).startswith("TRAINER")]
            if trainer_ids:
                gs["my_hand"] = hand + [random.choice(trainer_ids)]
                gs["my_deck_count"] = gs.get("my_deck_count", 60) - 1
        return True
    return False

