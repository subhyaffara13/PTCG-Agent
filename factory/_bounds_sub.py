def _synergy_score(card, core_elements, core_tags, details):
    base_ev = card.get("ev_score", 0.0)
    det = details.get(str(card["card_id"]), {}); synergy = 0.0
    if card.get("card_type") == "Pokemon" and core_elements:
        elem = det.get("element_type", "")
        if elem in core_elements or elem == "Colorless": synergy += 0.5
        else: synergy -= 0.5
    if set(card.get("combo_tags", [])) and core_tags and set(card.get("combo_tags", [])).intersection(core_tags):
        synergy += 0.2
    return base_ev + synergy

def _do_enforce_discard(self, legal, pool, deck, copies, ctr):
    import random
    src = [c for c in legal if "discard" in c.get("combo_tags", [])] or [c for c in pool if "discard" in c.get("combo_tags", [])]
    for _ in range(100):
        if ctr["discard"] >= 2 or not src: break
        self.add_card(random.choice(src), 1, deck, copies, ctr)

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

def _do_enforce_supporters(self, legal, pool, deck, copies, ctr):
    import random
    sp = [c for c in legal if self.is_supporter(c)] or [c for c in pool if self.is_supporter(c)]
    for _ in range(100):
        if ctr["supporter"] >= 8 or not sp: break
        self.add_card(random.choice(sp), 2, deck, copies, ctr)

def _do_fill_ok(self, c, deck, ctr, details):
    det = details.get(str(c["card_id"]), {}); ct = c.get("card_type")
    if ct == "Pokemon":
        stg = det.get("stage", "Basic")
        bc = sum(1 for d in deck if d.get("card_type") == "Pokemon" and details.get(str(d["card_id"]), {}).get("stage") == "Basic")
        s1 = sum(1 for d in deck if d.get("card_type") == "Pokemon" and details.get(str(d["card_id"]), {}).get("stage") == "Stage 1")
        s2 = sum(1 for d in deck if d.get("card_type") == "Pokemon" and details.get(str(d["card_id"]), {}).get("stage") == "Stage 2")
        if (stg == "Stage 2" and s2 + 1 > s1) or (stg == "Stage 1" and s1 + 1 > bc) or ctr["pkmn"] >= 18: return False
    elif ct == "Energy" and ctr["energy"] >= 12: return False
    elif self.is_supporter(c) and ctr["supporter"] >= 12: return False
    if det.get("stage") in ("Stage 1", "Stage 2"):
        prev = det.get("previous_stage")
        return not prev or any(d.get("card_name", "").lower() == prev.lower() for d in deck)
    return True
