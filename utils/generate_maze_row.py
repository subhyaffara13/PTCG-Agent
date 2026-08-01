
def generate_maze_row(rng, width, eller_state, door_probability):
    """Generate one maze row using Eller's algorithm on the left half, then mirror."""
    half = width // 2
    sets = list(eller_state["sets"])
    next_id = eller_state["next_set_id"]

    # Initialize unassigned columns
    for i in range(half):
        if sets[i] == 0:
            sets[i] = next_id
            next_id += 1

    # Left half walls: start with all walls
    left_walls = [WALL_N | WALL_E | WALL_S | WALL_W] * half

    # Horizontal merging: randomly remove E/W walls between adjacent cells in same row
    for c in range(half - 1):
        if sets[c] != sets[c + 1] and rng.random() < 0.5:
            # Merge: remove E wall from c and W wall from c+1
            left_walls[c] &= ~WALL_E
            left_walls[c + 1] &= ~WALL_W
            # Unify sets
            old_set = sets[c + 1]
            new_set = sets[c]
            for i in range(half):
                if sets[i] == old_set:
                    sets[i] = new_set

    # Vertical passages: for each set, ensure at least one cell has a south passage
    set_cells = defaultdict(list)
    for i in range(half):
        set_cells[sets[i]].append(i)

    next_row_sets = [0] * half
    for set_id, cells in set_cells.items():
        # Randomly assign south passages (prob 0.4), ensure at least one
        passages = [c for c in cells if rng.random() < 0.4]
        if not passages:
            passages = [rng.choice(cells)]
        for c in passages:
            left_walls[c] &= ~WALL_S  # Remove south wall
            next_row_sets[c] = set_id  # Keep set membership

    # Build full row by mirroring
    row_walls = [0] * width

    # Left half
    for c in range(half):
        row_walls[c] = left_walls[c]

    # Boundary: left edge always has west wall
    row_walls[0] |= WALL_W

    # Right half mirrors left half, swapping E and W
    for c in range(half):
        mirror_c = width - 1 - c
        w = left_walls[c]
        mirrored = 0
        if w & WALL_N:
            mirrored |= WALL_N
        if w & WALL_S:
            mirrored |= WALL_S
        if w & WALL_E:
            mirrored |= WALL_W  # E becomes W
        if w & WALL_W:
            mirrored |= WALL_E  # W becomes E
        row_walls[mirror_c] = mirrored

    # Boundary: right edge always has east wall
    row_walls[width - 1] |= WALL_E

    # Center wall between half-1 and half (with occasional doors)
    if rng.random() >= door_probability:
        row_walls[half - 1] |= WALL_E
        row_walls[half] |= WALL_W
    else:
        row_walls[half - 1] &= ~WALL_E
        row_walls[half] &= ~WALL_W

    # Mirror next_row_sets for the right half
    full_next_sets = [0] * width
    for c in range(half):
        full_next_sets[c] = next_row_sets[c]
    for c in range(half):
        mirror_c = width - 1 - c
        # Right half cells that had passages keep mirrored set ids
        if next_row_sets[c] != 0:
            full_next_sets[mirror_c] = next_row_sets[c] + 1000000  # Offset to avoid collision
        else:
            full_next_sets[mirror_c] = 0

    eller_state["sets"] = full_next_sets[:half]  # Only track left half
    eller_state["next_set_id"] = next_id

    return row_walls

