
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

