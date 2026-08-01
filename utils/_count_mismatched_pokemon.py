
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

