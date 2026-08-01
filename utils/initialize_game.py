
def initialize_game(state, env):
    """Set up the initial game state."""
    config = env.configuration
    obs = state[0].observation
    width = config.width
    height = config.height

    # The seed determines maze layout and scroll-time row generation -- both
    # hidden info that agents must not be able to predict. resolve_episode_seed
    # scrubs it from configuration and stashes it on env.info for the replay.
    seed = resolve_episode_seed(
        env,
        config_key="randomSeed",
        fallback=lambda: int(time.time() * 1000) % (2**31),
    )
    rng = Random(seed)

    # Initialize hidden state
    obs.nextUid = 0
    obs.scrollCounter = config.scrollStartInterval
    obs.globalWalls = {}
    obs.globalCrystals = {}
    obs.globalRobots = {}
    obs.globalMines = {}
    obs.globalMiningNodes = {}
    obs.southBound = 0
    obs.northBound = height - 1

    # Eller state for maze generation
    eller_state = {"sets": [0] * (width // 2), "next_set_id": 1}

    # Generate initial maze rows
    for row_num in range(height):
        row_walls = generate_maze_row(rng, width, eller_state, config.doorProbability)
        obs.globalWalls[str(row_num)] = row_walls
        if row_num > 0:
            ensure_wall_consistency(obs.globalWalls, row_num, width)
        place_crystals(
            rng,
            width,
            obs.globalCrystals,
            row_num,
            config.crystalDensity,
            config.crystalMinEnergy,
            config.crystalMaxEnergy,
        )
        place_mining_nodes(rng, width, obs.globalMiningNodes, row_num, config.miningNodeDensity, obs.globalCrystals)

    # First row: add south wall to all cells (boundary)
    for c in range(width):
        obs.globalWalls["0"][c] |= WALL_S

    obs.ellerState = eller_state

    # Place factories symmetrically
    p0_col = width // 4
    p1_col = width - 1 - p0_col
    factory_row = 2

    for player_idx, col in enumerate([p0_col, p1_col]):
        uid = create_uid(obs)
        obs.globalRobots[uid] = robot_to_list(
            {
                "type": FACTORY,
                "col": col,
                "row": factory_row,
                "energy": config.factoryEnergy,
                "owner": player_idx,
                "move_cooldown": 0,
                "jump_cooldown": 0,
                "build_cooldown": 0,
            }
        )

    # Initialize discovered cells per player
    obs.discoveredCells = [[], []]
    obs.discoveredMines = [[], []]

    # Compute initial vision
    for player_idx in range(2):
        player_robots = [list_to_robot(uid, data) for uid, data in obs.globalRobots.items() if data[4] == player_idx]
        visible = get_visible_cells(player_robots, config)
        obs.discoveredCells[player_idx] = [list(cell) for cell in visible]

    # Build per-player observations
    _update_player_observations(state, env)

    return state


def initialize_game(state, config):
    board_size = config.board_size
    starting_team_words = config.starting_team_words
    second_team_words = config.second_team_words
    
    # Load words
    dir_path = path.dirname(__file__)
    words_path = path.abspath(path.join(dir_path, "words.txt"))
    with open(words_path, "r") as f:
        all_words = [line.strip().upper() for line in f.readlines() if line.strip()]
        
    # Setup deterministic random generator if seed is provided.
    # When games_per_episode > 1, derive a fresh per-game seed from the base
    # seed so each game uses different words while the full sequence stays
    # reproducible from the original seed alone.
    seed = config.get("seed")
    current_game = state[0].observation.get("current_game", 0)
    if seed is not None:
        if current_game == 0:
            rng = random.Random(seed)
        else:
            master_rng = random.Random(seed)
            game_seed = 0
            for _ in range(current_game):
                game_seed = master_rng.randrange(2**32)
            rng = random.Random(game_seed)
    else:
        rng = random
        
    sampled_words = rng.sample(all_words, board_size)
    
    # Determine playing order and word counts
    starting_team = rng.choice(["blue", "yellow"])
    if starting_team == "blue":
        blue_count = starting_team_words
        yellow_count = second_team_words
    else:
        blue_count = second_team_words
        yellow_count = starting_team_words
    
    # Assign roles
    roles = ["blue"] * blue_count + ["yellow"] * yellow_count + ["trap"] * 1
    roles += ["neutral"] * (board_size - len(roles))
    rng.shuffle(roles)
    
    revealed = [False] * board_size
    
    for agent_state in state:
        agent_state.observation.words = sampled_words
        agent_state.observation.roles = roles[:]
        agent_state.observation.revealed = revealed[:]
        agent_state.observation.current_turn = 0 if starting_team == "blue" else 2
        agent_state.observation.clue = ""
        agent_state.observation.guesses_remaining = 0
        agent_state.observation.clue_number = 0

        initialize_memory(agent_state.observation, board_size)

