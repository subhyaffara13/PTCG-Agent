import random

def _mutate_map(map_rows, seed, num_mutations=_MUTATIONS_PER_MAP):
    """Apply small symmetric tile flips to a built-in map for variety.

    Each mutation picks a non-structural tile (plain/forest/mountain), changes
    it to a different terrain in the same set, and applies the same change at
    the point-symmetric position so the two starting sides stay balanced.
    """
    rng = random.Random(seed)
    rows = [list(r) for r in map_rows]
    height = len(rows)
    width = len(rows[0]) if height else 0

    candidates = [
        (x, y)
        for y in range(height)
        for x in range(width)
        if rows[y][x] in _MUTABLE_TERRAIN
    ]
    if not candidates:
        return rows

    applied = 0
    attempts = 0
    while applied < num_mutations and attempts < num_mutations * 10:
        attempts += 1
        x, y = rng.choice(candidates)
        mx, my = width - 1 - x, height - 1 - y
        # Skip the centre tile of odd-dimensioned maps (no distinct mirror) and
        # any cell whose mirror is structural (so we don't asymmetrically flip).
        if (x, y) == (mx, my) or rows[my][mx] not in _MUTABLE_TERRAIN:
            continue
        choices = [t for t in _MUTABLE_TERRAIN if t != rows[y][x]]
        new_tile = rng.choice(choices)
        rows[y][x] = new_tile
        rows[my][mx] = new_tile
        applied += 1

    return rows

