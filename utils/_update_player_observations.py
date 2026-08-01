
def _update_player_observations(state, env):
    """Build per-player observations from global state."""
    config = env.configuration
    obs = state[0].observation
    width = config.width
    south = obs.southBound
    north = obs.northBound
    window_height = north - south + 1

    for player_idx in range(2):
        # Get this player's robots
        player_robots = [list_to_robot(uid, data) for uid, data in obs.globalRobots.items() if data[4] == player_idx]

        # Compute current vision
        visible = get_visible_cells(player_robots, config)

        # Update discovered cells
        discovered = set()
        for cell in obs.discoveredCells[player_idx]:
            discovered.add((cell[0], cell[1]))
        discovered.update(visible)
        # Prune cells below south bound
        discovered = {(c, r) for c, r in discovered if r >= south}
        obs.discoveredCells[player_idx] = [list(cell) for cell in discovered]

        # Build walls array
        walls_array = [-1] * (window_height * width)
        for c, r in discovered:
            if south <= r <= north:
                idx = (r - south) * width + c
                row_key = str(r)
                if row_key in obs.globalWalls and 0 <= c < width:
                    walls_array[idx] = obs.globalWalls[row_key][c]

        # Build crystals (only currently visible)
        crystals = {}
        for c, r in visible:
            key = f"{c},{r}"
            if key in obs.globalCrystals:
                crystals[key] = obs.globalCrystals[key]

        # Build robots (own always visible, enemy only if in vision)
        robots = {}
        for uid, data in obs.globalRobots.items():
            col, row, owner = data[1], data[2], data[4]
            if owner == player_idx or (col, row) in visible:
                robots[uid] = list(data)

        # Build mines (discovered mines are remembered)
        # Update discovered mines with newly visible ones
        disc_mines = set()
        for key in obs.discoveredMines[player_idx]:
            disc_mines.add(key)
        for c, r in visible:
            key = f"{c},{r}"
            if key in obs.globalMines:
                disc_mines.add(key)
        # Remove mines that no longer exist
        disc_mines = {k for k in disc_mines if k in obs.globalMines}
        obs.discoveredMines[player_idx] = list(disc_mines)

        mines = {}
        for key in disc_mines:
            if key in obs.globalMines:
                mines[key] = list(obs.globalMines[key])

        # Build mining nodes (visible only, like crystals)
        mining_nodes = {}
        for c, r in visible:
            key = f"{c},{r}"
            if key in (obs.globalMiningNodes or {}):
                mining_nodes[key] = 1

        # Set per-player observation
        state[player_idx].observation.walls = walls_array
        state[player_idx].observation.crystals = crystals
        state[player_idx].observation.robots = robots
        state[player_idx].observation.mines = mines
        state[player_idx].observation.miningNodes = mining_nodes

