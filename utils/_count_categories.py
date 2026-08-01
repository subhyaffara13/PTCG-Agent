
def _count_categories(deck):
    from factory.deck_scorer_state import CardState
    basic = s1 = s2 = sup = item = eng = rec = 0; attackers = []
    supporters = {"judge", "professor's research", "iono", "boss's orders", "arven", "serena",
                  "colress's tenacity", "erika's invitation", "jacq", "nemona", "cynthia",
                  "marnie", "volkner", "skyla", "n", "juniper", "sycamore", "kiara"}
    for c in deck:
        if c.card_type == "Pokemon":
            if c.stage == "Basic": basic += 1
            elif c.stage == "Stage 1": s1 += 1
            elif c.stage == "Stage 2": s2 += 1
            if c.energy_cost > 0: attackers.append(c)
        elif c.card_type == "Energy": eng += 1
        elif c.card_type == "Trainer":
            name = c.card_name.lower()
            if "supporter" in c.combo_tags or any(s in name for s in supporters): sup += 1
            else: item += 1
        if "discard" in c.combo_tags: rec += 1
    return {"basic": basic, "s1": s1, "s2": s2, "sup": sup, "item": item,
            "eng": eng, "rec": rec, "attackers": attackers, "pkmn": basic + s1 + s2}

