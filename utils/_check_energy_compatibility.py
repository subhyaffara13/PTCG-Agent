
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

