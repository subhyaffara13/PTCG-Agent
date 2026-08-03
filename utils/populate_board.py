import copy
import math


def populate_board(state, env):
    obs = state[0].observation
    config = env.configuration
    size = env.configuration.size
    uid_counter = 0

    # Set seed for random number generators
    if not hasattr(config, "randomSeed"):
        max_int_32 = (1 << 31) - 1
        config.randomSeed = randrange(max_int_32)

    np.random.seed(config.randomSeed)
    seed(config.randomSeed)

    # This is a consistent way to generate unique strings to form ship and shipyard ids
    def create_uid():
        nonlocal uid_counter
        uid_counter += 1
        return f"{obs.step}-{uid_counter}"

    # Distribute Halite evenly into quartiles.
    half = math.ceil(size / 2)
    grid = [[0] * half for _ in range(half)]

    # Randomly place a few halite "seeds".
    for i in range(half):
        # random distribution across entire quartile
        grid[randint(0, half - 1)][randint(0, half - 1)] = i**2

        # as well as a particular distribution weighted toward the center of the map
        grid[randint(half // 2, half - 1)][randint(half // 2, half - 1)] = i**2

    # Spread the seeds radially.
    radius_grid = copy.deepcopy(grid)
    for r in range(half):
        for c in range(half):
            value = grid[r][c]
            if value == 0:
                continue

            # keep initial seed values, but constrain radius of clusters
            radius = min(round((value / half) ** 0.5), 1)
            for r2 in range(r - radius + 1, r + radius):
                for c2 in range(c - radius + 1, c + radius):
                    if 0 <= r2 < half and 0 <= c2 < half:
                        distance = (abs(r2 - r) ** 2 + abs(c2 - c) ** 2) ** 0.5
                        radius_grid[r2][c2] += int(value / max(1, distance) ** distance)

    # add some random sprouts of halite
    radius_grid = np.asarray(radius_grid)
    add_grid = np.random.gumbel(0, 300.0, size=(half, half)).astype(int)
    sparse_radius_grid = np.random.binomial(1, 0.5, size=(half, half))
    add_grid = np.clip(add_grid, 0, a_max=None) * sparse_radius_grid
    radius_grid += add_grid

    # add another set of random locations to the center corner
    corner_grid = np.random.gumbel(0, 500.0, size=(half // 4, half // 4)).astype(int)
    corner_grid = np.clip(corner_grid, 0, a_max=None)
    radius_grid[half - (half // 4) :, half - (half // 4) :] += corner_grid

    # Normalize the available halite against the defined configuration starting halite.
    total = sum([sum(row) for row in radius_grid])
    obs.halite = [0] * (size**2)
    for r, row in enumerate(radius_grid):
        for c, val in enumerate(row):
            val = int(val * config.startingHalite / total / 4)
            obs.halite[size * r + c] = val
            obs.halite[size * r + (size - c - 1)] = val
            obs.halite[size * (size - 1) - (size * r) + c] = val
            obs.halite[size * (size - 1) - (size * r) + (size - c - 1)] = val

    # Distribute the starting ships evenly.
    num_agents = len(state)
    starting_positions = [0] * num_agents
    if num_agents == 1:
        starting_positions[0] = size * (size // 2) + size // 2
    elif num_agents == 2:
        starting_positions[0] = size * (size // 2) + size // 4
        starting_positions[1] = size * (size // 2) + math.ceil(3 * size / 4) - 1
    elif num_agents == 4:
        starting_positions[0] = size * (size // 4) + size // 4
        starting_positions[1] = size * (size // 4) + 3 * size // 4
        starting_positions[2] = size * (3 * size // 4) + size // 4
        starting_positions[3] = size * (3 * size // 4) + 3 * size // 4

    # Initialize the players.
    obs.players = []
    for i in range(num_agents):
        ships = {create_uid(): [starting_positions[i], 0]}
        obs.players.append([state[0].reward, {}, ships])

    return state


def populate_board(state, env):
    obs = state[0].observation
    config = env.configuration
    size = env.configuration.size
    uid_counter = 0

    # Set seed for random number generators
    if not hasattr(config, "randomSeed"):
        max_int_32 = (1 << 31) - 1
        config.randomSeed = randrange(max_int_32)

    np.random.seed(config.randomSeed)
    seed(config.randomSeed)

    # This is a consistent way to generate unique strings to form ship and shipyard ids
    def create_uid():
        nonlocal uid_counter
        uid_counter += 1
        return f"{obs.step}-{uid_counter}"

    # Distribute Kore evenly into quartiles.
    half = math.ceil(size / 2)
    grid = [[0] * half for _ in range(half)]

    # Randomly place a few kore "seeds".
    for i in range(half):
        # random distribution across entire quartile
        grid[randint(0, half - 1)][randint(0, half - 1)] = i**2

        # as well as a particular distribution weighted toward the center of the map
        grid[randint(half // 2, half - 1)][randint(half // 2, half - 1)] = i**2

    # Spread the seeds radially.
    radius_grid = copy.deepcopy(grid)
    for r in range(half):
        for c in range(half):
            value = grid[r][c]
            if value == 0:
                continue

            # keep initial seed values, but constrain radius of clusters
            radius = min(round((value / half) ** 0.5), 1)
            for r2 in range(r - radius + 1, r + radius):
                for c2 in range(c - radius + 1, c + radius):
                    if 0 <= r2 < half and 0 <= c2 < half:
                        distance = (abs(r2 - r) ** 2 + abs(c2 - c) ** 2) ** 0.5
                        radius_grid[r2][c2] += int(value / max(1, distance) ** distance)

    # add some random sprouts of kore
    radius_grid = np.asarray(radius_grid)
    add_grid = np.random.gumbel(0, 300.0, size=(half, half)).astype(int)
    sparse_radius_grid = np.random.binomial(1, 0.5, size=(half, half))
    add_grid = np.clip(add_grid, 0, a_max=None) * sparse_radius_grid
    radius_grid += add_grid

    # add another set of random locations to the center corner
    corner_grid = np.random.gumbel(0, 500.0, size=(half // 4, half // 4)).astype(int)
    corner_grid = np.clip(corner_grid, 0, a_max=None)
    radius_grid[half - (half // 4) :, half - (half // 4) :] += corner_grid

    # make it assomptocially symmetric
    for i in range(half):
        for j in range(half):
            if i + j < half:
                radius_grid[i][j] = radius_grid[j][i]

    # Normalize the available kore against the defined configuration starting kore.
    total = sum([sum(row) for row in radius_grid])
    obs.kore = [0] * (size**2)
    for r, row in enumerate(radius_grid):
        for c, val in enumerate(row):
            val = int(val * config.startingKore / total / 4)
            obs.kore[size * r + c] = val
            obs.kore[size * r + (size - c - 1)] = val
            obs.kore[size * (size - 1) - (size * r) + c] = val
            obs.kore[size * (size - 1) - (size * r) + (size - c - 1)] = val

    # Distribute the starting shipyards evenly.
    num_agents = len(state)
    starting_positions = [0] * num_agents
    if num_agents == 1:
        starting_positions[0] = size * (size // 2) + size // 2
    elif num_agents == 2:
        starting_positions[0] = size * (size // 2 - size // 4) + size // 4
        starting_positions[1] = size * (size // 2 + size // 4) + math.ceil(3 * size / 4) - 1
    elif num_agents == 4:
        starting_positions[0] = size * (size // 4 + 1) + size // 4 - 1
        starting_positions[1] = size * (size // 4 - 1) + 3 * size // 4 - 1
        starting_positions[2] = size * (3 * size // 4 + 1) + size // 4 + 1
        starting_positions[3] = size * (3 * size // 4 - 1) + 3 * size // 4 + 1

    # clear the kore on the starting square
    for pos in starting_positions:
        obs.kore[pos] = 0

    # Initialize the players.
    obs.players = []
    for i in range(num_agents):
        shipyards = {create_uid(): [starting_positions[i], 0, 0]}
        obs.players.append([state[0].reward, shipyards, {}])

    return state

