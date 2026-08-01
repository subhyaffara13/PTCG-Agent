
def renderer(state, env):
    return json.dumps(Battle.obs)


def renderer(state, env):
    columns = env.configuration.columns
    rows = env.configuration.rows
    board = state[0].observation.board

    def print_row(values, delim="|"):
        return f"{delim} " + f" {delim} ".join(str(v) for v in values) + f" {delim}\n"

    row_bar = "+" + "+".join(["---"] * columns) + "+\n"
    out = row_bar
    for r in range(rows):
        out = out + print_row(board[r * columns : r * columns + columns]) + row_bar

    return out


def renderer(state, env):
    config = env.configuration
    width = config.width
    obs = state[0].observation
    south = obs.southBound
    north = obs.northBound

    g_walls = obs.globalWalls or {}
    g_robots = obs.globalRobots or {}
    g_mines = obs.globalMines or {}
    g_crystals = obs.globalCrystals or {}

    TYPE_CHAR = {FACTORY: "F", SCOUT: "S", WORKER: "W", MINER: "M"}

    # Build cell content map
    cell_content = {}

    for uid, data in g_robots.items():
        rtype, col, row, energy, owner = data[0], data[1], data[2], data[3], data[4]
        cell_content[(col, row)] = f"{TYPE_CHAR[rtype]}{owner}"

    for key, data in g_mines.items():
        col, row = int(key.split(",")[0]), int(key.split(",")[1])
        if (col, row) not in cell_content:
            cell_content[(col, row)] = f"m{data[2]}"

    g_mining_nodes = obs.globalMiningNodes or {}
    for key in g_mining_nodes:
        col, row = int(key.split(",")[0]), int(key.split(",")[1])
        if (col, row) not in cell_content:
            cell_content[(col, row)] = " <> "

    for key, energy in g_crystals.items():
        col, row = int(key.split(",")[0]), int(key.split(",")[1])
        if (col, row) not in cell_content:
            cell_content[(col, row)] = f"*{min(energy, 99)}"

    out = ""
    for row in range(north, south - 1, -1):
        row_key = str(row)
        rw = g_walls.get(row_key, [0] * width)

        # Top border (north walls)
        top = f"{row:3d} +"
        for col in range(width):
            w = rw[col] if col < len(rw) else 0
            top += "----+" if (w & WALL_N) else "    +"
        out += top + "\n"

        # Cell row
        cell_line = "    "
        for col in range(width):
            w = rw[col] if col < len(rw) else 0
            wall_char = "|" if (w & WALL_W) else " "
            content = cell_content.get((col, row), "")
            cell_line += wall_char + content.center(4)
        # Right edge
        last_w = rw[width - 1] if width - 1 < len(rw) else 0
        cell_line += "|" if (last_w & WALL_E) else " "
        out += cell_line + "\n"

    # Bottom border
    bottom = "    +"
    south_key = str(south)
    if south_key in g_walls:
        rw = g_walls[south_key]
        for col in range(width):
            w = rw[col] if col < len(rw) else 0
            bottom += "----+" if (w & WALL_S) else "    +"
    else:
        bottom += "----+" * width
    out += bottom + "\n"

    out += f"\nStep: {obs.step}  South: {south}  North: {north}\n"
    for uid, data in g_robots.items():
        rtype, col, row, energy, owner = data[0], data[1], data[2], data[3], data[4]
        tname = TYPE_NAMES[rtype]
        out += f"  {uid}: P{owner} {tname} ({col},{row}) E={energy}\n"

    return out


def renderer(state, env):
    html_renderer(env)


def renderer(state, env):
    config = env.configuration
    size = config.size
    obs = state[0].observation

    board = [[h, -1, -1, -1] for h in obs.halite]
    for index, player in enumerate(obs.players):
        _, shipyards, ships = player
        for shipyard_pos in shipyards.values():
            board[int(shipyard_pos)][1] = index
        for ship in ships.values():
            ship_pos, ship_halite = ship
            board[int(ship_pos)][2] = index
            board[int(ship_pos)][3] = ship_halite

    col_divider = "|"
    row_divider = "+" + "+".join(["----"] * size) + "+\n"

    out = row_divider
    for row in range(size):
        for col in range(size):
            _, _, ship, ship_halite = board[col + row * size]
            out += col_divider + (f"{min(int(ship_halite), 99)}S{ship}" if ship > -1 else "").ljust(4)
        out += col_divider + "\n"
        for col in range(size):
            halite, shipyard, _, _ = board[col + row * size]
            if shipyard > -1:
                out += col_divider + f"SY{shipyard}".ljust(4)
            else:
                out += col_divider + str(min(int(halite), 9999)).rjust(4)
        out += col_divider + "\n" + row_divider

    return out


def renderer(state, env):
    config = env.configuration
    columns = config.columns
    rows = config.rows

    food_symbol = "F"
    column_divider = "|"
    row_divider = "+" + "+".join(["---"] * columns) + "+\n"

    board = [" "] * (rows * columns)
    for pos in state[0].observation.food:
        board[pos] = food_symbol

    for index, goose in enumerate(state[0].observation.geese):
        for position in goose:
            board[position] = index

    out = row_divider
    for row in range(rows):
        for col in range(columns):
            out += column_divider + f" {board[(row * columns) + col]} "
        out += column_divider + "\n" + row_divider

    return out


def renderer(state, env):
    obs = state[0].observation
    out = f"Step {get(obs, 'step', 0)}  Day {get(obs, 'day', 0)}  Hour {get(obs, 'hour', 0)}\n"
    market = get(obs, "market", {}) or {}
    town = get(obs, "town", {}) or {}
    out += f"Town shops: {town.get('unlocked_shops', [])}\n"
    out += "Prices: " + ", ".join(f"{k}=${v}" for k, v in (market.get("prices", {}) or {}).items()) + "\n"
    for i, s in enumerate(state):
        farm = obs.farms[i] if i < len(obs.farms) else None
        if farm is None:
            continue
        priv = get(s.observation, "private", {}) or {}
        out += (
            f"Player {i}: ${farm['money']:.0f}  farmer={farm['farmer']}  "
            f"hands={len(farm['hands'])}  unlocked={farm['unlocked_quadrants']}  "
            f"shed={priv.get('shed')}  seeds={priv.get('seeds')}\n"
        )
        for row in farm["tiles"]:
            out += "  " + " ".join(_render_tile(t) for t in row) + "\n"
    return out


def renderer(state, env):
    obs = state[0].observation
    out = f"Step {get(obs, 'step', 0)}  Day {get(obs, 'day', 0)}  Hour {get(obs, 'hour', 0)}\n"
    for i, farm in enumerate(get(obs, "farms", []) or []):
        out += f"Player {i}: ${farm['money']:.0f}  farmer={farm['farmer']}  seeds={farm['seeds']}\n"
        for row in farm["tiles"]:
            cells = []
            for tile in row:
                cells.append("." if tile is None else tile["crop"][0])
            out += "  " + " ".join(cells) + "\n"
    return out


def renderer(state, env):
    config = env.configuration
    size = config.size
    obs = state[0].observation

    board = [[h, -1, -1, -1] for h in obs.kore]
    for index, player in enumerate(obs.players):
        _, shipyards, fleets = player
        for shipyard in shipyards.values():
            shipyard_pos, _, _ = shipyard
            board[shipyard_pos][1] = index
        for fleet in fleets.values():
            fleet_pos, fleet_kore, ship_count, _, _ = fleet
            board[fleet_pos][2] = index
            board[fleet_pos][3] = ship_count

    col_divider = "|"
    row_divider = "+" + "+".join(["----"] * size) + "+\n"

    out = row_divider
    for row in range(size):
        for col in range(size):
            _, _, fleet, fleet_kore = board[col + row * size]
            out += col_divider + (f"{min(int(fleet_kore), 99)}S{fleet}" if fleet > -1 else "").ljust(4)
        out += col_divider + "\n"
        for col in range(size):
            kore, shipyard, _, _ = board[col + row * size]
            if shipyard > -1:
                out += col_divider + f"SY{shipyard}".ljust(4)
            else:
                out += col_divider + str(min(int(kore), 9999)).rjust(4)
        out += col_divider + "\n" + row_divider

    return out


def renderer(state, env):
    raise NotImplementedError("To render the replay, please set the render mode to json or html")


def renderer(state, env):
    raise NotImplementedError("To render the replay, please set the render mode to json or html")


def renderer(steps, env):
    rounds_played = len(env.steps)
    board = ""

    for i in range(1, rounds_played):
        actions = [agent.action for agent in steps[i]]
        rewards = [agent.reward for agent in steps[i]]
        board += f"Round {i} Actions: {actions}, Rewards: {rewards}\n"

    return board


def renderer(state: list[utils.Struct], env: core.Environment) -> str:
    """Kaggle environment text renderer."""
    if hasattr(env, "os_state"):
        return str(env.os_state)
    else:
        return "Game state uninitialized."


def renderer(state, env):
    obs = state[0].observation
    out = f"Step {get(obs, 'step', 0)}\n"
    out += "Planets:\n"
    for p in get(obs, "planets", []):
        out += f"  ID: {p[0]}, Owner: {p[1]}, Pos: ({p[2]:.1f}, {p[3]:.1f}), R: {p[4]:.1f}, Ships: {p[5]}, Prod: {p[6]}\n"
    out += "Fleets:\n"
    for f in get(obs, "fleets", []):
        out += f"  ID: {f[0]}, Owner: {f[1]}, Pos: ({f[2]:.1f}, {f[3]:.1f}), Angle: {f[4]:.2f}, Ships: {f[6]}\n"
    return out


def renderer(state, env):
    obs = state[0].observation
    step = _get(obs, "step", 0)
    out = [f"Turn {step} / {env.configuration.episodeSteps}"]
    out.append("Planets:")
    for p in _get(obs, "planets", []) or []:
        out.append(f"  {p[0]:3d}  owner={p[3]}  ships={p[4]:4d}  growth={p[5]}  ({p[1]:6.2f}, {p[2]:6.2f})")
    fleets = _get(obs, "fleets", []) or []
    out.append(f"Fleets ({len(fleets)}):")
    for f in fleets:
        out.append(f"  owner={f[0]}  ships={f[1]:4d}  {f[2]}->{f[3]}  turns_left={f[5]}/{f[4]}")
    return "\n".join(out) + "\n"


def renderer(state, env):
    """Return an ASCII text representation of the current board."""
    if not state or len(state) < 2:
        return "No state available."

    obs = state[0].observation
    board = obs.board if hasattr(obs, "board") else []
    units_list = obs.units if hasattr(obs, "units") else []
    gold = obs.gold if hasattr(obs, "gold") else [0, 0]
    turn = obs.turnNumber if hasattr(obs, "turnNumber") else 0

    if not board:
        return "Board not initialised."

    # Build unit lookup
    unit_map = {}
    for u in units_list:
        unit_map[(u["x"], u["y"])] = u

    # Tile display characters
    tile_chars = {
        "p": ".",
        "w": "~",
        "m": "^",
        "f": "T",
        "r": "=",
        "b": "B",
        "h": "H",
        "t": "#",
        "o": "~",
    }

    lines = []
    lines.append(f"Turn {turn}  |  P1 Gold: {gold[0]}  |  P2 Gold: {gold[1]}")
    lines.append(f"P1 Status: {state[0].status}  |  P2 Status: {state[1].status}")
    lines.append("")

    for y, row in enumerate(board):
        line = ""
        for x, cell in enumerate(row):
            pos = (x, y)
            if pos in unit_map:
                u = unit_map[pos]
                # Show unit type with player indicator (lowercase=p1, uppercase=p2)
                ch = u["type"]
                line += ch.lower() if u["owner"] == 1 else ch.upper()
            else:
                line += tile_chars.get(cell, "?")
        lines.append(line)

    return "\n".join(lines)


def renderer(state, env):
    sign_names = ["Rock", "Paper", "Scissors", "Spock", "Lizard"]
    rounds_played = len(env.steps)
    board = ""

    # This line prints results each round, good for debugging
    for i in range(1, rounds_played):
        step = env.steps[i]
        right_move = step[0].observation.lastOpponentAction
        left_move = step[1].observation.lastOpponentAction
        board += f"Round {i}: {sign_names[left_move]} vs {sign_names[right_move]}, Score: {step[0].reward} to {step[1].reward}\n"

    board += f"Game ended on round {rounds_played - 1}, final score: {state[0].reward} to {state[0].reward}\n"
    return board


def renderer(state, env):
    if not hasattr(env, "moderator") or not hasattr(env, "game_state"):
        return "Game not initialized by interpreter yet."

    game_state: GameState = env.game_state

    lines = []
    for entry in game_state.consume_messages():
        lines.append(entry.description)
    return "\n\n".join(lines)


def renderer(state, env):
    words = state[0].observation.words
    revealed = state[0].observation.revealed
    roles = state[0].observation.roles
    
    out = ""
    for r in range(5):
        row_str = ""
        for c in range(5):
            idx = r * 5 + c
            w = words[idx]
            if revealed[idx]:
                w = f"[{roles[idx].upper()[0]}] {w}"
            else:
                w = f"({roles[idx].upper()[0]}) {w}"
            row_str += f"{w:<15}"
        out += row_str + "\n"
    
    out += f"\nTurn: {state[0].observation.current_turn}\n"
    out += f"Clue: {state[0].observation.clue} ({state[0].observation.guesses_remaining} remaining)\n"
    return out

