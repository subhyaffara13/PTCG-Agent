
def generate_maze_layout(maze_size: int, rf_size: int) -> chex.Array:
    """Generate array representation of maze layout with walls."""
    # Need to add wall offset if receptive field size is large
    rf_offset = int((rf_size - 1) / 2)

    # Need to add surrounding outer walls - first row
    maze = rf_offset * [(maze_size + 2 * rf_offset) * "x"]

    # Add inidividual rows with walls
    row_with_walls = (
        rf_offset * "x" + int((maze_size + 1) / 2) * " x" + (rf_offset - 1) * "x"
    )
    row_without_walls = rf_offset * "x" + maze_size * " " + rf_offset * "x"
    for r in range(maze_size):
        if r % 2 == 0:
            maze.append(row_without_walls)
        else:
            maze.append(row_with_walls)
    # Need to add surrounding outer walls - last row
    for _ in range(rf_offset):
        maze.append((maze_size + 2 * rf_offset) * "x")

    # Transform into boolean array map
    bool_map = []
    for row in maze:
        bool_map.append([r == " " for r in row])
    return jnp.array(bool_map)

