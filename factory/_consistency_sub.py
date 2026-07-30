import logging
logger = logging.getLogger(__name__)

def _check_energy_compatibility(deck, ct):
    has_fire = any("fire" in e.lower() or "{r}" in e.lower() for e in {c.card_name for c in deck if c.card_type == "Energy"})
    has_lightning = any("lightning" in e.lower() or "{l}" in e.lower() for e in {c.card_name for c in deck if c.card_type == "Energy"})
    has_grass = any("grass" in e.lower() or "{g}" in e.lower() for e in {c.card_name for c in deck if c.card_type == "Energy"})
    has_fighting = any("fighting" in e.lower() or "{f}" in e.lower() for e in {c.card_name for c in deck if c.card_type == "Energy"})
    has_water = any("water" in e.lower() or "{w}" in e.lower() for e in {c.card_name for c in deck if c.card_type == "Energy"})
    has_psychic = any("psychic" in e.lower() or "{p}" in e.lower() for e in {c.card_name for c in deck if c.card_type == "Energy"})
    has_metal = any("metal" in e.lower() or "{m}" in e.lower() for e in {c.card_name for c in deck if c.card_type == "Energy"})
    has_dark = any("dark" in e.lower() or "{d}" in e.lower() for e in {c.card_name for c in deck if c.card_type == "Energy"})
    return has_fire, has_lightning, has_grass, has_fighting, has_water, has_psychic, has_metal, has_dark

def _count_mismatched_pokemon(deck, has_grass, has_water, has_psychic, has_metal, has_dark):
    mismatched = 0
    for c in deck:
        if c.card_type != "Pokemon" or c.energy_cost <= 0: continue
        elem = (c.element_type or c.card_name).lower()
        needs_grass = "grass" in elem or "{g}" in elem or "ogerpon" in c.card_name
        needs_water = "water" in elem or "{w}" in elem
        needs_psychic = "psychic" in elem or "{p}" in elem
        needs_metal = "metal" in elem or "{m}" in elem
        needs_dark = "dark" in elem or "{d}" in elem
        if (needs_grass and not has_grass) or (needs_water and not has_water) or            (needs_psychic and not has_psychic) or (needs_metal and not has_metal) or            (needs_dark and not has_dark): mismatched += 1
    return mismatched

def _draw_supporter_penalty(deck, cs):
    draw_supporters_count = sum(1 for c in deck if c.card_type == "Trainer" and
        any(k in c.card_name.lower() for k in {"research", "lillie", "carmine", "professor"}))
    has_recovery = any("pad" in c.card_name.lower() or "stretcher" in c.card_name.lower() or
        "rod" in c.card_name.lower() for c in deck)
    if draw_supporters_count >= 4 and not has_recovery:
        cs = max(0.0, cs - 0.2)
    return cs
