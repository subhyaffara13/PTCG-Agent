
def place_mining_nodes(rng, width, nodes, row_num, density, crystals):
    """Place mining nodes on a row. Symmetric: left half mirrored to right. Avoids crystal cells."""
    half = width // 2
    for c in range(half):
        if rng.random() < density:
            key = f"{c},{row_num}"
            mirror_c = width - 1 - c
            mirror_key = f"{mirror_c},{row_num}"
            if key in crystals or mirror_key in crystals:
                continue
            nodes[key] = 1
            if mirror_c != c:
                nodes[mirror_key] = 1

