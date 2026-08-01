
def place_crystals(rng, width, crystals, row_num, density, min_e, max_e):
    """Place crystals on a row. Symmetric: left half mirrored to right."""
    half = width // 2
    for c in range(half):
        if rng.random() < density:
            energy = rng.randint(min_e, max_e)
            crystals[f"{c},{row_num}"] = energy
            mirror_c = width - 1 - c
            if mirror_c != c:
                crystals[f"{mirror_c},{row_num}"] = energy

