"""
factory/deck_generator_helpers.py

Core helpers for deck generation: probability math, card addition,
signature injection, evolution pyramids, consistency trainers,
bounds enforcement, and fill-to-60 logic.
"""
import math
import random

def hypergeometric_setup_prob(deck_size: int, basics_count: int, hand_size: int = 7) -> float:
    """Probability of drawing at least one Basic Pokémon in opening hand."""
    if deck_size <= 0 or basics_count <= 0 or hand_size <= 0:
        return 0.0
    try:
        return 1.0 - math.comb(deck_size - basics_count, hand_size) / math.comb(deck_size, hand_size)
    except (ValueError, ZeroDivisionError):
        return 0.0

def is_supporter(card: dict) -> bool:
    return card.get("card_type") == "Trainer" and "Supporter" in card.get("combo_tags", [])

def add_card(card: dict, count: int, deck: list, copies: dict, ctr: dict) -> int:
    """Add copies of a card, respecting 4-copy rule (99 for basic energy). Returns added count."""
    cid = str(card["card_id"])
    mx = 99 if card.get("card_type") == "Energy" and "Basic" in card.get("card_name", "") else 4
    added = 0
    for _ in range(count):
        if len(deck) < 60 and copies.get(cid, 0) < mx:
            deck.append(dict(card)); copies[cid] = copies.get(cid, 0) + 1; added += 1
            ct = card.get("card_type")
            if ct == "Pokemon": ctr["pkmn"] += 1
            elif ct == "Energy": ctr["energy"] += 1
            if is_supporter(card): ctr["supporter"] += 1
            if "discard" in card.get("combo_tags", []): ctr["discard"] += 1
    return added

def inject_signature_cards(arch, id_map, name_map, deck, copies, ctr):
    """Add archetype signature and card_pool cards (2 copies each)."""
    for sid in arch.get("signature_cards", []) + arch.get("card_pool", []):
        s = str(sid)
        if s in id_map: add_card(id_map[s], 2, deck, copies, ctr)
        elif s.lower() in name_map: add_card(name_map[s.lower()], 2, deck, copies, ctr)

def inject_evolution_pyramids(deck, details, name_map, copies, ctr):
    """Ensure evolution lines have proper pyramid (Basic > Stage 1 > Stage 2)."""
    for pkmn in [c for c in deck if c.get("card_type") == "Pokemon"]:
        det = details.get(str(pkmn["card_id"]), {})
        if det.get("stage") == "Stage 2":
            p1 = det.get("previous_stage")
            if p1 and p1.lower() in name_map:
                add_card(name_map[p1.lower()], 3, deck, copies, ctr)
                p0 = details.get(str(name_map[p1.lower()]["card_id"]), {}).get("previous_stage")
                if p0 and p0.lower() in name_map: add_card(name_map[p0.lower()], 4, deck, copies, ctr)
        elif det.get("stage") == "Stage 1":
            p0 = det.get("previous_stage")
            if p0 and p0.lower() in name_map: add_card(name_map[p0.lower()], 4, deck, copies, ctr)

def inject_consistency_trainers(deck, details, id_map, name_map, copies, ctr):
    """Add search/draw trainers; include Rare Candy if Stage 2 lines exist."""
    ids = {"1121": 4, "ultra-ball-sv1-196": 4, "nest-ball-sv1-255": 4,
           "1102": 4, "professor-s-research-sv1-190": 4, "1086": 4, "iono-pal-185": 4, "1213": 4}
    names = {"ultra ball": 4, "nest ball": 4, "professor's research": 4,
             "iono": 4, "switch": 2, "boss's orders": 2}
    if any(details.get(str(c["card_id"]), {}).get("stage") == "Stage 2"
           for c in deck if c.get("card_type") == "Pokemon"):
        ids.update({"rare-candy-sv1-191": 4, "1079": 4})
    for tid, tc in ids.items():
        if tid in id_map: add_card(id_map[tid], tc, deck, copies, ctr)
    for tn, tc in names.items():
        if tn in name_map: add_card(name_map[tn], tc, deck, copies, ctr)

def enforce_bounds(legal, basics, name_map, deck, copies, ctr, pool, details):
    """Ensure minimum counts for discard recovery, Pokémon, and supporters."""
    # Discard recovery
    src = [c for c in legal if "discard" in c.get("combo_tags", [])] or \
          [c for c in pool if "discard" in c.get("combo_tags", [])]
    for _ in range(100):
        if ctr["discard"] >= 2 or not src: break
        add_card(random.choice(src), 1, deck, copies, ctr)
    # Pokémon count
    pp = [c for c in legal if c.get("card_type") == "Pokemon"] or \
         [c for c in pool if c.get("card_type") == "Pokemon"]
    for _ in range(100):
        if ctr["pkmn"] >= 12 or not pp: break
        ch = random.choice(pp); det = details.get(str(ch["card_id"]), {})
        if det.get("stage") != "Basic":
            prev = det.get("previous_stage")
            if prev and prev.lower() in name_map: add_card(name_map[prev.lower()], 2, deck, copies, ctr)
        add_card(ch, 2, deck, copies, ctr)
    # Supporters
    sp = [c for c in legal if is_supporter(c)] or [c for c in pool if is_supporter(c)]
    for _ in range(100):
        if ctr["supporter"] >= 8 or not sp: break
        add_card(random.choice(sp), 2, deck, copies, ctr)
    # Guarantee at least one Basic
    if not any(details.get(str(c["card_id"]), {}).get("stage") == "Basic"
               for c in deck if c.get("card_type") == "Pokemon") and basics:
        add_card(random.choice(basics), 3, deck, copies, ctr)

def fill_to_60(legal, matching, deck, copies, ctr, details):
    """Fill deck to 60 cards respecting pyramid constraints."""
    m_ids = {str(e["card_id"]) for e in matching}
    cands = [c for c in sorted(legal, key=lambda x: x.get("ev_score", 0.0), reverse=True)
             if c.get("card_type") != "Energy" or str(c["card_id"]) in m_ids]
    _cs = lambda s: sum(1 for d in deck if d.get("card_type") == "Pokemon" and details.get(str(d["card_id"]), {}).get("stage") == s)
    for _ in range(5000):
        if len(deck) >= 60 or not cands: break
        c = random.choice(cands); det = details.get(str(c["card_id"]), {}); ct = c.get("card_type")
        if ct == "Pokemon":
            sg = det.get("stage", "Basic")
            if (sg == "Stage 2" and _cs("Stage 2") + 1 >= _cs("Stage 1")) or \
               (sg == "Stage 1" and _cs("Stage 1") + 1 >= _cs("Basic")) or ctr["pkmn"] >= 18: continue
        elif ct == "Energy" and ctr["energy"] >= 12: continue
        elif is_supporter(c) and ctr["supporter"] >= 12: continue
        if det.get("stage") in ("Stage 1", "Stage 2"):
            prev = det.get("previous_stage")
            if not prev or any(d.get("card_name", "").lower() == prev.lower() for d in deck):
                add_card(c, 1, deck, copies, ctr)
        else: add_card(c, 1, deck, copies, ctr)
