import random
from scratch.deck_genetics import get_card_copy_limit

def make_deck(lines, trainers, energies, basics, pool, details) -> list:
    deck, copies = [], {}
    def add(c, count):
        cid = str(c["card_id"])
        limit = get_card_copy_limit(c)
        added = 0
        for _ in range(count):
            if len(deck) < 60 and copies.get(cid, 0) < limit:
                deck.append(c)
                copies[cid] = copies.get(cid, 0) + 1
                added += 1
        return added

    allowed_types = {details.get(str(p["card_id"]), {}).get("element_type", "") for p in lines}
    allowed_types.discard("")
    if not allowed_types:
        allowed_types.add("{L}")

    t_map = {"{R}": "{R}", "{W}": "{W}", "{G}": "{G}", "{L}": "{L}", "{F}": "{F}", "{P}": "{P}", "{D}": "{D}", "{M}": "{M}"}
    allowed_energy_keywords = [t_map.get(t, "none") for t in allowed_types]

    # Snap in the Attacker Package
    for p in lines:
        add(p, 3)
        prev = details.get(str(p["card_id"]), {}).get("previous_stage")
        if prev:
            p_prev = next((x for x in pool if x.get("card_name", "").lower() == prev.lower()), None)
            if p_prev:
                add(p_prev, 4)
                prev_prev = details.get(str(p_prev["card_id"]), {}).get("previous_stage")
                if prev_prev:
                    p_basic = next((x for x in pool if x.get("card_name", "").lower() == prev_prev.lower()), None)
                    if p_basic:
                        add(p_basic, 4)

    # Snap in an Engine Package
    def norm(n): return n.lower().replace("'", "'").replace("é", "e")
    
    engine_packages = [
        {"ultra ball": 4, "professor's research": 4, "boss's orders": 3, "switch": 2},
        {"buddy-buddy poffin": 4, "iono": 4, "nest ball": 3, "super rod": 2},
        {"arven": 4, "rare candy": 4, "ultra ball": 4, "boss's orders": 2}
    ]
    chosen_engine = random.choice(engine_packages)
    
    # Add base trainers + chosen engine
    combined_trainers = dict(trainers)
    for t, count in chosen_engine.items():
        combined_trainers[t] = max(combined_trainers.get(t, 0), count)

    for t, tc in combined_trainers.items():
        match_t = next((x for x in pool if norm(x.get("card_name", "")) == norm(t)), None)
        if match_t:
            add(match_t, tc)

    matching_energies = []
    for kw in allowed_energy_keywords:
        match_e = [e for e in energies if kw in e.get("card_name", "")]
        if match_e:
            matching_energies.extend(match_e)
    if not matching_energies:
        matching_energies = [e for e in energies if "{L}" in e.get("card_name", "")] or energies

    for e in matching_energies[:2]:
        add(e, 6)

    unique_pokemon = list({str(p["card_id"]): p for p in deck if p.get("card_type") == "Pokemon"}.values())
    for p in unique_pokemon:
        add(p, 4)

    loop_limit = 100
    while len(deck) < 60 and sum(1 for c in deck if c.get("card_type") == "Energy") < 14 and loop_limit > 0:
        loop_limit -= 1
        add(random.choice(matching_energies), 1)

    matching_basics = [b for b in basics if details.get(str(b["card_id"]), {}).get("element_type") in allowed_types]
    if not matching_basics:
        matching_basics = basics
    shuffled_basics = list(matching_basics)
    random.shuffle(shuffled_basics)
    for cand_p in shuffled_basics:
        if len(deck) >= 60:
            break
        add(cand_p, 4)

    while len(deck) < 60:
        deck.append(random.choice(matching_energies))

    return deck[:60]
