
def _do_enforce_pokemon(self, legal, pool, name_map, deck, copies, ctr, details):
    import random
    pp = [c for c in legal if c.get("card_type") == "Pokemon"] or [c for c in pool if c.get("card_type") == "Pokemon"]
    for _ in range(100):
        if ctr["pkmn"] >= 12 or not pp: break
        ch = random.choice(pp); det = details.get(str(ch["card_id"]), {})
        if det.get("stage") == "Basic": self.add_card(ch, 2, deck, copies, ctr)
        else:
            prev = det.get("previous_stage")
            if prev and prev.lower() in name_map: self.add_card(name_map[prev.lower()], 2, deck, copies, ctr)
            self.add_card(ch, 2, deck, copies, ctr)

