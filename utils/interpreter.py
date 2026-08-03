import copy
import json
import random
import sys
import uuid
from typing import Any
import math


def interpreter(state, env):
    if env.done:
        Battle.battle_ptr = None
        for i in range(2):
            state[i].status = "ACTIVE"
            o = state[i].observation
            o["select"] = None
            o["logs"] = []
            o["current"] = None
            o["search_begin_input"] = None
        return state
    elif Battle.battle_ptr == None:
        decks = [state[0].action, state[1].action]
        error = False
        for i in range(2):
            if state[i].status == "TIMEOUT" or state[i].status == "ERROR":
                error = True
                continue
            if len(decks[i]) != 60:
                state[i].status = "INVALID"
                env.steps[0][0]["error"] = f"Player {i}'s deck does not have 60 cards."
                error = True
        if not error:
            _, start_data = battle_start(state[0].action, state[1].action)
            if start_data.errorPlayer >= 0:
                state[start_data.errorPlayer].status = "INVALID"
                env.steps[0][0]["error"] = f"Player {i}'s deck error."
                error = True
        if error:
            for i in range(2):
                if state[i].status == "ACTIVE":
                    state[i].status = "DONE"
            return state
        if Battle.battle_ptr == None:
            raise ValueError("battle_ptr None.")
    else:
        error = False
        select_player = Battle.obs["current"]["yourIndex"]
        if state[select_player].status == "TIMEOUT" or state[select_player].status == "ERROR":
            error = True
        else:
            try:
                battle_select(state[select_player].action)
            except:
                state[select_player].status = "INVALID"
                error = True

        if error:
            state[select_player].reward = -1
            state[1 - select_player].status = "DONE"
            state[1 - select_player].reward = 1
            finish(state, env)
            return state

    obs = Battle.obs
    s = obs["current"]
    if s["result"] >= 0:
        state[0].status = "DONE"
        state[1].status = "DONE"
        if s["result"] == 0:
            state[0].reward = 1
            state[1].reward = -1
        elif s["result"] == 1:
            state[0].reward = -1
            state[1].reward = 1
        else:
            state[0].reward = 0
            state[1].reward = 0
        finish(state, env)
    else:
        index = s["yourIndex"]
        state[index].status = "ACTIVE"
        state[1 - index].status = "INACTIVE"
        o = state[index].observation
        o["select"] = obs["select"]
        o["logs"] = obs["logs"]
        o["current"] = obs["current"]
        o["search_begin_input"] = obs["search_begin_input"]
    return state


def interpreter(state, env):
    columns = env.configuration.columns
    rows = env.configuration.rows

    # Ensure the board is properly initialized.
    board = state[0].observation.board
    if len(board) != (rows * columns):
        board = [EMPTY] * (rows * columns)
        state[0].observation.board = board

    if env.done:
        return state

    # Isolate the active and inactive agents.
    active = state[0] if state[0].status == "ACTIVE" else state[1]
    inactive = state[0] if state[0].status == "INACTIVE" else state[1]
    if active.status != "ACTIVE" or inactive.status != "INACTIVE":
        active.status = "DONE" if active.status == "ACTIVE" else active.status
        inactive.status = "DONE" if inactive.status == "INACTIVE" else inactive.status
        return state

    # Active agent action.
    column = active.action

    # Invalid column, agent loses.
    if column < 0 or active.action >= columns or board[column] != EMPTY:
        active.status = f"Invalid column: {column}"
        inactive.status = "DONE"
        return state

    # Mark the position.
    play(board, column, active.observation.mark, env.configuration)

    # Check for a win.
    if is_win(board, column, active.observation.mark, env.configuration):
        active.reward = 1
        active.status = "DONE"
        inactive.reward = -1
        inactive.status = "DONE"
        return state

    # Check for a tie.
    if all(mark != EMPTY for mark in board):
        active.status = "DONE"
        inactive.status = "DONE"
        return state

    # Swap active agents to switch turns.
    active.status = "INACTIVE"
    inactive.status = "ACTIVE"

    return state


def interpreter(state, env):
    obs = state[0].observation
    config = env.configuration

    if env.done:
        return initialize_game(state, env)

    # Deserialize robots from global state
    robots = {}
    for uid, data in obs.globalRobots.items():
        robots[uid] = list_to_robot(uid, data)

    walls = obs.globalWalls
    crystals = obs.globalCrystals if obs.globalCrystals else {}
    mines = obs.globalMines if obs.globalMines else {}
    mining_nodes = obs.globalMiningNodes if obs.globalMiningNodes else {}
    width = config.width
    south = obs.southBound
    north = obs.northBound

    # Collect actions from both players
    actions = {}
    for player_idx in range(2):
        player_actions = state[player_idx].action
        if player_actions and isinstance(player_actions, dict):
            actions.update(player_actions)

    # --- Phase 0: Cooldown tick ---
    for uid, r in robots.items():
        if r["move_cooldown"] > 0:
            r["move_cooldown"] -= 1
        if r["jump_cooldown"] > 0:
            r["jump_cooldown"] -= 1
        if r["build_cooldown"] > 0:
            r["build_cooldown"] -= 1

    # --- Phase 1: Action validation ---
    validated_actions = {}
    for uid, action in actions.items():
        if uid not in robots:
            continue
        r = robots[uid]
        if not isinstance(action, str):
            continue

        valid = False
        rtype = r["type"]

        if action == "IDLE":
            valid = True
        elif action in MOVE_DIRS:
            valid = True  # Movement validity checked later with cooldowns/walls
        elif action in JUMP_ACTIONS:
            valid = rtype == FACTORY
        elif action in WALL_BUILD_ACTIONS or action in WALL_REMOVE_ACTIONS:
            valid = rtype == WORKER
        elif action == "TRANSFORM":
            valid = rtype == MINER
        elif action in FACTORY_BUILD_ACTIONS:
            valid = rtype == FACTORY
        elif action in TRANSFER_ACTIONS:
            valid = True

        if valid:
            validated_actions[uid] = action
        else:
            validated_actions[uid] = "IDLE"

    # UIDs not in actions default to IDLE
    for uid in robots:
        if uid not in validated_actions:
            validated_actions[uid] = "IDLE"

    # --- Phase 2: Energy consumption ---
    energy_depleted = set()
    for uid, r in robots.items():
        r["energy"] -= config.energyPerTurn
        if r["energy"] < 0:
            r["energy"] = 0
        if r["energy"] == 0:
            energy_depleted.add(uid)

    # Robots with no energy can't act (forced IDLE)
    for uid in energy_depleted:
        validated_actions[uid] = "IDLE"

    # --- Phase 3: Special actions ---
    destroyed = set()

    # 3a: TRANSFORM (Miner -> Mine, requires mining node)
    for uid in list(robots.keys()):
        if uid in destroyed:
            continue
        if validated_actions.get(uid) != "TRANSFORM":
            continue
        r = robots[uid]
        key = f"{r['col']},{r['row']}"
        if key not in mining_nodes:
            validated_actions[uid] = "IDLE"
            continue
        if r["energy"] < config.transformCost:
            validated_actions[uid] = "IDLE"
            continue
        mine_energy = min(r["energy"] - config.transformCost, config.mineMaxEnergy)
        mines[key] = [mine_energy, config.mineMaxEnergy, r["owner"], config.mineRate]
        # Remove the mining node (consumed)
        del mining_nodes[key]
        destroyed.add(uid)

    # 3b: BUILD_DIR / REMOVE_DIR (Worker toggles wall in direction)
    # Worker survives. Costs `wallBuildCost` (BUILD_*) or `wallRemoveCost`
    # (REMOVE_*) regardless of effect (no-op if the wall already exists for
    # BUILD or doesn't exist for REMOVE, or if the wall is fixed). Out-of-bounds
    # neighbor (off the map) is also a no-op but still charges. Insufficient
    # energy → IDLE, no charge.
    for uid in list(robots.keys()):
        if uid in destroyed:
            continue
        action = validated_actions.get(uid, "IDLE")
        is_build = action in WALL_BUILD_ACTIONS
        is_remove = action in WALL_REMOVE_ACTIONS
        if not (is_build or is_remove):
            continue
        r = robots[uid]
        cost = config.wallBuildCost if is_build else config.wallRemoveCost
        if r["energy"] < cost:
            validated_actions[uid] = "IDLE"
            continue
        r["energy"] -= cost
        direction = action.split("_")[1]
        col, row = r["col"], r["row"]
        row_key = str(row)
        if is_fixed_wall(col, direction, width):
            continue  # charged, no effect
        bit = DIR_WALL_BIT[direction]
        opp_bit = DIR_WALL_BIT[OPPOSITE_DIR[direction]]
        dc, dr = DIR_OFFSETS[direction]
        nc, nr = col + dc, row + dr
        nr_key = str(nr)
        neighbor_in_map = 0 <= nc < width and nr_key in walls
        if is_build:
            if row_key in walls:
                walls[row_key][col] |= bit
            if neighbor_in_map:
                walls[nr_key][nc] |= opp_bit
        else:  # is_remove
            if row_key in walls:
                walls[row_key][col] &= ~bit
            if neighbor_in_map:
                walls[nr_key][nc] &= ~opp_bit

    # 3d: BUILD (Factory spawns robot in the chosen direction; combat resolves
    # in Phase 4). `BUILD_<UNIT>` (no suffix) defaults to NORTH for backward
    # compatibility; `BUILD_<UNIT>_<DIR>` spawns in that direction.
    for uid in list(robots.keys()):
        if uid in destroyed:
            continue
        action = validated_actions.get(uid, "IDLE")
        if action not in FACTORY_BUILD_ACTIONS:
            continue
        r = robots[uid]

        parts = action.split("_")
        unit_key = parts[1]
        direction = parts[2] if len(parts) > 2 else "NORTH"

        new_type = FACTORY_BUILD_UNITS[unit_key]
        if new_type == SCOUT:
            cost = config.scoutCost
        elif new_type == WORKER:
            cost = config.workerCost
        else:  # MINER
            cost = config.minerCost
        new_energy = cost

        if r["energy"] < cost:
            validated_actions[uid] = "IDLE"
            continue
        if r["build_cooldown"] > 0:
            validated_actions[uid] = "IDLE"
            continue

        dc, dr = DIR_OFFSETS[direction]
        sc, sr = r["col"] + dc, r["row"] + dr

        # Check wall between factory and spawn cell
        if not can_move_through(walls, width, r["col"], r["row"], direction):
            validated_actions[uid] = "IDLE"
            continue
        # Spawn cell must be within the active window and the map width.
        if sr > north or sr < south or sc < 0 or sc >= width:
            validated_actions[uid] = "IDLE"
            continue

        r["energy"] -= cost
        r["build_cooldown"] = config.factoryBuildCooldown
        new_uid = create_uid(obs)
        new_period = get_move_period(new_type, config)
        robots[new_uid] = {
            "uid": new_uid,
            "type": new_type,
            "col": sc,
            "row": sr,
            "energy": new_energy,
            "owner": r["owner"],
            "move_cooldown": new_period,
            "jump_cooldown": 0,
            "build_cooldown": 0,
        }
        validated_actions[new_uid] = "IDLE"

    # 3e: TRANSFER
    for uid in list(robots.keys()):
        if uid in destroyed:
            continue
        action = validated_actions.get(uid, "IDLE")
        if action not in TRANSFER_ACTIONS:
            continue
        r = robots[uid]
        direction = action.split("_")[1]
        if not can_move_through(walls, width, r["col"], r["row"], direction):
            continue
        dc, dr = DIR_OFFSETS[direction]
        tc, tr = r["col"] + dc, r["row"] + dr
        # Find friendly robot at target
        target_uid = None
        for tuid, tr_robot in robots.items():
            if tuid in destroyed:
                continue
            if tr_robot["col"] == tc and tr_robot["row"] == tr and tr_robot["owner"] == r["owner"] and tuid != uid:
                target_uid = tuid
                break
        if target_uid is None:
            continue
        target = robots[target_uid]
        max_e = get_robot_max_energy(target["type"], config)
        transfer_amount = r["energy"]
        space = max_e - target["energy"]
        if space != float("inf"):
            transfer_amount = min(transfer_amount, max(0, int(space)))
        target["energy"] += transfer_amount
        r["energy"] -= transfer_amount

    # Remove destroyed robots
    for uid in destroyed:
        del robots[uid]

    # --- Phase 4: Movement + combat resolution ---
    movements = {}  # uid -> (target_col, target_row)
    stationary_uids = set()
    off_board_destroyed = set()  # units that walked/jumped off the N/S edge

    for uid, r in robots.items():
        action = validated_actions.get(uid, "IDLE")

        if action in MOVE_DIRS:
            if r["move_cooldown"] > 0:
                stationary_uids.add(uid)
                continue
            direction = action
            dc, dr_off = DIR_OFFSETS[direction]
            tc, tr = r["col"] + dc, r["row"] + dr_off
            if not (south <= tr <= north):
                # Off-board N/S move: only the source cell's wall can block.
                # (can_move_through also requires the neighbor row to exist,
                # which is false off the edge.) E/W is impossible here because
                # perimeter walls always block.
                row_key = str(r["row"])
                source_wall = walls.get(row_key, [0] * width)[r["col"]] if 0 <= r["col"] < width else 0
                if source_wall & DIR_WALL_BIT[direction]:
                    stationary_uids.add(uid)
                else:
                    off_board_destroyed.add(uid)
                continue
            if can_move_through(walls, width, r["col"], r["row"], direction):
                movements[uid] = (tc, tr)
            else:
                stationary_uids.add(uid)

        elif action in JUMP_ACTIONS:
            if r["move_cooldown"] > 0 or r["jump_cooldown"] > 0:
                stationary_uids.add(uid)
                continue
            direction = action.split("_")[1]
            dc, dr_off = DIR_OFFSETS[direction]
            tc, tr = r["col"] + dc * 2, r["row"] + dr_off * 2
            # Jump always happens (no wall check). Off-board landing kills the
            # factory; cooldown is consumed either way.
            r["jump_cooldown"] = config.factoryJumpCooldown
            if 0 <= tc < width and south <= tr <= north and str(tr) in walls:
                movements[uid] = (tc, tr)
            else:
                off_board_destroyed.add(uid)
        else:
            stationary_uids.add(uid)

    # Remove off-board units before combat resolution.
    for uid in off_board_destroyed:
        if uid in robots:
            del robots[uid]

    # Build position map for stationary robots
    position_map = defaultdict(list)  # (col, row) -> [uid, ...]
    for uid in stationary_uids:
        if uid in robots:
            r = robots[uid]
            position_map[(r["col"], r["row"])].append(uid)

    # Group movements by target cell; also include cells with multiple
    # stationary robots (e.g. from spawn collisions) so combat resolves.
    target_groups = defaultdict(list)  # (col, row) -> [mover_uid, ...]
    for uid, (tc, tr) in movements.items():
        target_groups[(tc, tr)].append(uid)
    for pos, uids in position_map.items():
        if len(uids) > 1 and pos not in target_groups:
            target_groups[pos] = []  # no movers, but multiple occupants

    move_destroyed = set()
    moved = set()
    combat_cells = set()  # cells where a multi-robot collision happened

    for target, mover_uids in target_groups.items():
        occupant_uids = position_map.get(target, [])
        all_uids = mover_uids + occupant_uids

        if len(all_uids) <= 1:
            if mover_uids:
                moved.add(mover_uids[0])
            continue

        # Multi-robot collision: apply crush rules. Friendly fire is real —
        # ownership doesn't matter. Factories are indestructible vs anything
        # except an enemy factory (mutual destruction).
        combat_cells.add(target)
        survivors = set()
        destroyed_in_combat = set()
        all_types = [(uid, robots[uid]["type"]) for uid in all_uids]

        factory_uids = [uid for uid, rtype in all_types if rtype == FACTORY]
        factory_owners = {robots[uid]["owner"] for uid in factory_uids}
        factories_mutual = len(factory_owners) > 1

        for uid, rtype in all_types:
            if rtype == FACTORY:
                if factories_mutual:
                    destroyed_in_combat.add(uid)
                else:
                    survivors.add(uid)
                continue
            crushed = False
            for other_uid, other_type in all_types:
                if other_uid == uid:
                    continue
                if (other_type, rtype) in CRUSHES:
                    crushed = True
                    break
                elif other_type == rtype:
                    # Same type → both destroyed (mutual), regardless of owner.
                    crushed = True
                    destroyed_in_combat.add(other_uid)
                    break
            if crushed:
                destroyed_in_combat.add(uid)
            else:
                survivors.add(uid)

        move_destroyed.update(destroyed_in_combat)
        for uid in mover_uids:
            if uid in survivors:
                moved.add(uid)

    # Apply movements
    for uid in moved:
        if uid in move_destroyed:
            continue
        if uid in movements:
            tc, tr = movements[uid]
            robots[uid]["col"] = tc
            robots[uid]["row"] = tr
            period = get_move_period(robots[uid]["type"], config)
            robots[uid]["move_cooldown"] = period

    # Remove combat casualties (factories only die via mutual factory destruction)
    for uid in move_destroyed:
        if uid in robots:
            del robots[uid]

    # Consume crystals at combat cells where no robot survived.
    # (If a robot did survive, Phase 5 will hand it the crystal energy.)
    for (cc, cr_) in combat_cells:
        ckey = f"{cc},{cr_}"
        if ckey not in crystals:
            continue
        survivor_here = any(r["col"] == cc and r["row"] == cr_ for r in robots.values())
        if not survivor_here:
            del crystals[ckey]

    # --- Phase 5: Crystal collection ---
    crystals_to_remove = []
    for uid, r in robots.items():
        key = f"{r['col']},{r['row']}"
        if key in crystals:
            max_e = get_robot_max_energy(r["type"], config)
            space = max_e - r["energy"]
            if space == float("inf"):
                r["energy"] += crystals[key]
            else:
                r["energy"] += min(crystals[key], int(space))
            crystals_to_remove.append(key)
    for key in crystals_to_remove:
        if key in crystals:
            del crystals[key]

    # --- Phase 6: Mine energy fill ---
    for uid, r in robots.items():
        key = f"{r['col']},{r['row']}"
        if key in mines and mines[key][2] == r["owner"]:
            mine = mines[key]
            max_e = get_robot_max_energy(r["type"], config)
            space = max_e - r["energy"]
            if space == float("inf"):
                transfer = mine[0]
            else:
                transfer = min(mine[0], int(space))
            r["energy"] += transfer
            mine[0] -= transfer

    # --- Phase 7: Mine energy generation ---
    for key, mine in mines.items():
        mine[0] = min(mine[0] + mine[3], mine[1])

    # --- Phase 8: Scroll advancement ---
    # Pull the hidden seed from env.info (see initialize_game). Falling back
    # to 0 keeps determinism if env.info is somehow missing.
    env_info = getattr(env, "info", None) or {}
    episode_seed = env_info.get("seed", 0) or 0
    rng = Random(episode_seed + obs.step)
    obs.scrollCounter = obs.scrollCounter - 1
    if obs.scrollCounter <= 0:
        obs.southBound += 1
        obs.northBound += 1
        south = obs.southBound
        north = obs.northBound

        # Generate new north row
        eller_state = obs.ellerState
        if isinstance(eller_state, dict):
            pass
        else:
            eller_state = dict(eller_state)
            eller_state["sets"] = list(eller_state["sets"])

        new_row_walls = generate_maze_row(rng, width, eller_state, config.doorProbability)
        walls[str(north)] = new_row_walls
        ensure_wall_consistency(walls, north, width)
        obs.ellerState = eller_state

        place_crystals(
            rng,
            width,
            crystals,
            north,
            config.crystalDensity,
            config.crystalMinEnergy,
            config.crystalMaxEnergy,
        )
        place_mining_nodes(rng, width, mining_nodes, north, config.miningNodeDensity, crystals)

        # Clean up old rows
        old_key = str(south - 1)
        if old_key in walls:
            del walls[old_key]

        obs.scrollCounter = get_scroll_interval(obs.step, config)

    # --- Phase 9: Boundary destruction ---
    south = obs.southBound
    boundary_destroyed = set()
    factory_destroyed = [False, False]

    for uid, r in list(robots.items()):
        if r["row"] < south:
            if r["type"] == FACTORY:
                factory_destroyed[r["owner"]] = True
            boundary_destroyed.add(uid)

    for uid in boundary_destroyed:
        del robots[uid]

    # Remove mines below boundary
    mine_keys_to_remove = [key for key in mines if int(key.split(",")[1]) < south]
    for key in mine_keys_to_remove:
        del mines[key]

    # Remove crystals below boundary
    crystal_keys_to_remove = [key for key in crystals if int(key.split(",")[1]) < south]
    for key in crystal_keys_to_remove:
        del crystals[key]

    # Remove mining nodes below boundary
    node_keys_to_remove = [key for key in mining_nodes if int(key.split(",")[1]) < south]
    for key in node_keys_to_remove:
        del mining_nodes[key]

    # --- Phase 10: Win condition check ---
    # Check if any player has no factory
    for player_idx in range(2):
        has_factory = any(r["type"] == FACTORY and r["owner"] == player_idx for r in robots.values())
        if not has_factory and state[player_idx].status == "ACTIVE":
            factory_destroyed[player_idx] = True

    if factory_destroyed[0] and factory_destroyed[1]:
        # Both eliminated same turn - tiebreak via energy → unit count → draw
        r0, r1 = _resolve_tiebreak(robots)
        state[0].reward = r0
        state[1].reward = r1
        state[0].status = "DONE"
        state[1].status = "DONE"
    elif factory_destroyed[0]:
        state[0].reward = obs.step - config.episodeSteps - 1
        state[1].reward = sum(r["energy"] for r in robots.values() if r["owner"] == 1)
        state[0].status = "DONE"
        state[1].status = "DONE"
    elif factory_destroyed[1]:
        state[1].reward = obs.step - config.episodeSteps - 1
        state[0].reward = sum(r["energy"] for r in robots.values() if r["owner"] == 0)
        state[0].status = "DONE"
        state[1].status = "DONE"
    elif obs.step + 2 >= config.episodeSteps:
        # Time limit: both factories alive on the final interpreter call →
        # tiebreak via energy → unit count → draw.
        r0, r1 = _resolve_tiebreak(robots)
        state[0].reward = r0
        state[1].reward = r1
        state[0].status = "DONE"
        state[1].status = "DONE"

    # --- Phase 12: Update rewards for active players ---
    for player_idx in range(2):
        if state[player_idx].status == "ACTIVE":
            total = sum(r["energy"] for r in robots.values() if r["owner"] == player_idx)
            state[player_idx].reward = total

    # --- Serialize robots back to global state ---
    obs.globalRobots = {uid: robot_to_list(r) for uid, r in robots.items()}
    obs.globalCrystals = crystals
    obs.globalMines = mines
    obs.globalMiningNodes = mining_nodes
    obs.globalWalls = walls

    # --- Phase 11: Update per-player observations ---
    _update_player_observations(state, env)

    return state


def interpreter(state, env):
    global m_envs
    if "id" not in env.configuration or env.configuration.id is None:
        env.configuration.id = str(uuid.uuid4())

    if (env.configuration.id not in m_envs) or env.done:
        if env.configuration.id not in m_envs:
            print(
                "Staring a new environment %s: with scenario: %s"
                % (env.configuration.id, env.configuration.scenario_name)
            )

            other_config_options = {}
            # Use webm to encode videos (so that you can see them in the browser).
            other_config_options["video_format"] = "webm"
            if env.configuration.running_in_notebook:
                assert not env.configuration.render, "Render is not supported inside notebook environment."

            env.football_video_path = None
            if "TeamNames" in env.info:
                names = env.info["TeamNames"]
                assert len(names) == 2
                other_config_options["custom_display_stats"] = [
                    "LEFT PLAYER: %s" % names[0],
                    "RIGHT PLAYER: %s" % names[1],
                ]
            m_envs[env.configuration.id] = football_env().create_environment(
                env_name=env.configuration.scenario_name,
                stacked=False,
                # We use 'raw' representation to transfer data between server and agents.
                representation="raw",
                logdir=path.join(env.configuration.logdir, env.configuration.id),
                write_goal_dumps=False,
                write_full_episode_dumps=env.configuration.save_video,
                write_video=env.configuration.save_video,
                render=env.configuration.render,
                number_of_left_players_agent_controls=env.configuration.team_1,
                number_of_right_players_agent_controls=env.configuration.team_2,
                other_config_options=other_config_options,
            )
        else:
            print(
                "Resetting environment %s: with scenario: %s" % (env.configuration.id, env.configuration.scenario_name)
            )
        obs = m_envs[env.configuration.id].reset()
        update_observations_and_rewards(configuration=env.configuration, state=state, obs=obs)
    if env.done:
        return state

    if maybe_terminate(env, state):
        return state

    # verify actions.
    controlled_players = env.configuration.team_1
    action_set = football_action_set.action_set_dict["default"]

    try:
        for action in state[0].action:
            football_action_set.named_action_from_action_set(action_set, action)
    except Exception:
        mark_invalid(state[0], "Invalid action provided: %s." % state[0].action)
    if len(state[0].action) != env.configuration.team_1:
        mark_invalid(
            state[0],
            "Invalid number of actions provided: Expected %d, got %d."
            % (env.configuration.team_1, len(state[0].action)),
        )
    actions_to_env = state[0].action

    try:
        for action in state[1].action:
            football_action_set.named_action_from_action_set(action_set, action)
    except Exception:
        mark_invalid(state[1], "Invalid action provided: %s." % state[1].action)
    if len(state[1].action) != env.configuration.team_2:
        mark_invalid(
            state[1],
            "Invalid number of actions provided: Expected %d, got %d."
            % (env.configuration.team_2, len(state[1].action)),
        )
    if env.configuration.team_2:
        actions_to_env = actions_to_env + state[1].action

    if maybe_terminate(env, state):
        return state
    obs, rew, done, info = m_envs[env.configuration.id].step(actions_to_env)

    if "dumps" in info:
        env.football_video_path = retrieve_video_link(info["dumps"])
    update_observations_and_rewards(
        configuration=env.configuration, state=state, obs=obs, rew=obs[0]["score"][0] - obs[0]["score"][1]
    )

    ## TODO: pass other information from 'info' to the state/agent.
    if done:
        for agent in range(2):
            state[agent].status = "DONE"
        try_get_video(env)

    return state


def interpreter(state, env):
    obs = state[0].observation
    config = env.configuration

    # Initialize the board (place cell halite and starting ships).
    if env.done:
        return populate_board(state, env)

    # Interpreter invoked here
    actions = [agent.action for agent in state]
    board = Board(obs, config, actions)
    board = board.next()
    state[0].observation = obs = utils.structify(board.observation)

    # Remove players with invalid status or insufficient potential.
    for index, agent in enumerate(state):
        player_halite, shipyards, ships = obs.players[index]
        if agent.status == "ACTIVE" and len(ships) == 0 and (len(shipyards) == 0 or player_halite < config.spawnCost):
            # Agent can no longer gather any halite
            agent.status = "DONE"
            agent.reward = board.step - board.configuration.episode_steps - 1
        if agent.status != "ACTIVE" and agent.status != "DONE":
            obs.players[index] = [0, {}, {}]

    # Check if done (< 2 players and num_agents > 1)
    if len(state) > 1 and sum(1 for agent in state if agent.status == "ACTIVE") < 2:
        for agent in state:
            if agent.status == "ACTIVE":
                agent.status = "DONE"

    # Update Rewards.
    for index, agent in enumerate(state):
        if agent.status == "ACTIVE":
            agent.reward = obs.players[index][0]
        elif agent.status != "DONE":
            agent.reward = 0

    return state


def interpreter(state, env):
    configuration = Configuration(env.configuration)
    columns = configuration.columns
    rows = configuration.rows
    min_food = configuration.min_food
    state[0].observation = shared_observation = Observation(state[0].observation)

    # Reset the environment.
    if env.done:
        agent_count = len(state)
        heads = sample(range(columns * rows), agent_count)
        shared_observation["geese"] = [[head] for head in heads]
        food_candidates = set(range(columns * rows)).difference(heads)
        # Ensure we only place as many food as there are open squares
        min_food = min(min_food, len(food_candidates))
        shared_observation["food"] = sample(list(food_candidates), min_food)
        return state

    geese = shared_observation.geese
    food = shared_observation.food

    # If there is no last state, reuse current state so that current action is never the opposite of the last action.
    last_state = env.steps[-1] if len(env.steps) > 1 else state
    # Apply the actions from active agents.
    for index, agent in enumerate(state):
        if agent.status != "ACTIVE":
            if agent.status != "INACTIVE" and agent.status != "DONE":
                # ERROR, INVALID, or TIMEOUT, remove the goose.
                geese[index] = []
            continue

        action = Action[agent.action]

        # Check action direction
        last_agent = last_state[index]
        last_action = Action[last_agent["action"]] if "action" in last_agent else action
        if last_action == action.opposite():
            env.debug_print(f"Opposite action: {agent.observation.index, action, last_action}")
            agent.status = "DONE"
            geese[index] = []
            continue

        goose = geese[index]
        head = translate(goose[0], action, columns, rows)

        # Consume food or drop a tail piece.
        if head in food:
            food.remove(head)
        else:
            goose.pop()

        # Self collision.
        if head in goose:
            env.debug_print(f"Body Hit: {agent.observation.index, action, head, goose}")
            agent.status = "DONE"
            geese[index] = []
            continue

        while len(goose) >= configuration.max_length:
            # Free a spot for the new head if needed
            goose.pop()
        # Add New Head to the Goose.
        goose.insert(0, head)

        # If hunger strikes remove from the tail.
        if len(env.steps) % configuration.hunger_rate == 0:
            if len(goose) > 0:
                goose.pop()
            if len(goose) == 0:
                env.debug_print(f"Goose Starved: {action}")
                agent.status = "DONE"
                continue

    goose_positions = histogram(position for goose in geese for position in goose)

    # Check for collisions.
    for index, agent in enumerate(state):
        goose = geese[index]
        if len(goose) > 0:
            head = geese[index][0]
            if goose_positions[head] > 1:
                env.debug_print(f"Goose Collision: {agent.action}")
                agent.status = "DONE"
                geese[index] = []

    # Add food if min_food threshold reached.
    needed_food = min_food - len(food)
    if needed_food > 0:
        collisions = {position for goose in geese for position in goose}
        available_positions = set(range(rows * columns)).difference(collisions).difference(food)
        # Ensure we don't sample more food than available positions.
        needed_food = min(needed_food, len(available_positions))
        food.extend(sample(list(available_positions), needed_food))

    # Set rewards after deleting all geese to ensure that geese don't receive a reward on the turn they perish.
    for index, agent in enumerate(state):
        if agent.status == "ACTIVE":
            # Adding 1 to len(env.steps) ensures that if an agent gets reward 4507, it died on turn 45 with length 7.
            agent.reward = (len(env.steps) + 1) * (configuration.max_length + 1) + len(geese[index])

    # If only one ACTIVE agent left, set it to DONE.
    active_agents = [a for a in state if a.status == "ACTIVE"]
    if len(active_agents) == 1:
        agent = active_agents[0]
        agent.status = "DONE"

    return state


def interpreter(state, env):
    num_agents = len(state)
    obs0 = state[0].observation

    if not hasattr(obs0, "farms") or not obs0.farms:
        _initialize(state, env)
        return state

    if env.done:
        return state

    cfg = env.configuration
    turns_per_day = max(1, int(get(cfg, "turnsPerDay", 24)))
    board_size = int(get(cfg, "boardSize", 10))
    shed_capacity = int(get(cfg, "shedCapacity", 100))

    step = get(obs0, "step", 0)
    day = step // turns_per_day

    for i, s in enumerate(state):
        action = s.action if isinstance(s.action, dict) else {}
        farmer_action = action.get("farmer", ["PASS"]) if isinstance(action, dict) else ["PASS"]
        hands_actions = action.get("hands", []) if isinstance(action, dict) else []
        if not isinstance(hands_actions, list):
            hands_actions = []

        # Atomic PLANT validation: if total PLANT requests for a crop this turn
        # exceed available seeds, drop ALL PLANT requests for that crop.
        unit_actions = [farmer_action, *hands_actions]
        plant_demand = {}
        for a in unit_actions:
            if isinstance(a, list) and len(a) >= 2 and a[0] == "PLANT":
                plant_demand[a[1]] = plant_demand.get(a[1], 0) + 1
        seeds = s.observation.private.get("seeds", {}) if hasattr(s.observation.private, "get") else {}
        blocked = {crop for crop, n in plant_demand.items() if n > seeds.get(crop, 0)}

        def _allowed(a):
            if isinstance(a, list) and len(a) >= 2 and a[0] == "PLANT" and a[1] in blocked:
                return ["PASS"]
            return a

        _apply_unit_action(obs0.farms[i], s.observation.private, 0, _allowed(farmer_action),
                           board_size, day, turns_per_day, shed_capacity)
        for h_idx, hand_action in enumerate(hands_actions):
            _apply_unit_action(obs0.farms[i], s.observation.private, h_idx + 1,
                               _allowed(hand_action), board_size, day, turns_per_day, shed_capacity)

    _process_market(state, env)
    _town_consume(env, state, step)
    for farm in obs0.farms:
        _decay_plants(farm, step)
    if (step + 1) % turns_per_day == 0:
        _end_of_day(state, env, day)

    next_step = step + 1
    obs0.day = next_step // turns_per_day
    obs0.hour = next_step % turns_per_day
    for i in range(1, num_agents):
        state[i].observation.farms = obs0.farms
        state[i].observation.market = obs0.market
        state[i].observation.town = obs0.town
        state[i].observation.day = obs0.day
        state[i].observation.hour = obs0.hour

    # `step` here is the previous step counter; framework records the post-interpreter
    # state at the next index. -2 fires DONE on the final recorded step.
    if step >= cfg.episodeSteps - 2:
        for s in state:
            s.status = "DONE"
            s.reward = float(obs0.farms[s.observation.player]["money"])

    return state


def interpreter(state, env):
    num_agents = len(state)
    obs0 = state[0].observation

    if not hasattr(obs0, "farms") or not obs0.farms:
        _initialize(state, env)
        return state

    if env.done:
        return state

    configuration = env.configuration
    turns_per_day = max(1, int(get(configuration, "turnsPerDay", 24)))
    board_size = int(get(configuration, "boardSize", 5))
    max_orders = max(1, int(get(configuration, "maxMarketOrdersPerTurn", 10)))

    step = get(obs0, "step", 0)
    day = step // turns_per_day

    for i, s in enumerate(state):
        action = s.action if isinstance(s.action, dict) else {}
        farmer_action = action.get("farmer", ["PASS"]) if isinstance(action, dict) else ["PASS"]
        result = _apply_farmer_action(obs0.farms[i], farmer_action, board_size, day, turns_per_day)
        if result is not None:
            crop_name, units = result
            obs0.farms[i]["money"] += float(CROPS[crop_name]["price"] * units)

    _process_market(state, max_orders)

    for farm in obs0.farms:
        _decay_plants(farm, step)

    if (step + 1) % turns_per_day == 0:
        for farm in obs0.farms:
            _daily_refresh(farm, day, turns_per_day)

    next_step = step + 1
    obs0.day = next_step // turns_per_day
    obs0.hour = next_step % turns_per_day
    for i in range(1, num_agents):
        state[i].observation.farms = obs0.farms
        state[i].observation.day = obs0.day
        state[i].observation.hour = obs0.hour

    if step >= configuration.episodeSteps - 2:
        for s in state:
            s.status = "DONE"
            s.reward = float(obs0.farms[s.observation.player]["money"])

    return state


def interpreter(state, env):
    obs = state[0].observation
    config = env.configuration

    # Initialize the board (place cell kore and starting ships).
    if env.done:
        return populate_board(state, env)

    # Interpreter invoked here
    actions = [agent.action for agent in state]
    board = Board(obs, config, actions)
    board = board.next()
    state[0].observation = obs = utils.structify(board.observation)

    # Remove players with invalid status or insufficient potential.
    for index, agent in enumerate(state):
        player_kore, shipyards, fleets = obs.players[index]
        ships_in_shipyards = [int(s[1]) for s in shipyards.values()]
        can_spawn = len(shipyards) > 0 and player_kore >= config.spawnCost
        if agent.status == "ACTIVE" and len(shipyards) == 0 and len(fleets) == 0:
            # Agent can no longer gather any kore
            agent.status = "DONE"
            agent.reward = board.step - board.configuration.episode_steps - 1
        if agent.status == "ACTIVE" and ships_in_shipyards == 0 and len(fleets) == 0 and not can_spawn:
            # Agent can no longer gather any kore
            agent.status = "DONE"
            agent.reward = board.step - board.configuration.episode_steps - 1
        if agent.status != "ACTIVE" and agent.status != "DONE":
            obs.players[index] = [0, {}, {}]

    # Check if done (< 2 players and num_agents > 1)
    if len(state) > 1 and sum(1 for agent in state if agent.status == "ACTIVE") < 2:
        for agent in state:
            if agent.status == "ACTIVE":
                agent.status = "DONE"

    # Update Rewards.
    for index, agent in enumerate(state):
        if agent.status == "ACTIVE":
            agent.reward = obs.players[index][0]
        elif agent.status != "DONE":
            agent.reward = 0

    return state


def interpreter(state, env):
    global dimension_process, game_state, t, q, prev_step
    player1 = state[0]
    player2 = state[1]

    ### 1.1: Initialize dimensions in the background within the orchestrator if we haven't already ###
    if dimension_process is None:
        # dimension_process = Popen(["ts-node", "-P", path.abspath(path.join(dir_path, "dimensions/tsconfig.json")), path.abspath(path.join(dir_path, "dimensions/run.ts"))], stdin=PIPE, stdout=PIPE)
        try:
            dimension_process = Popen(
                ["node", path.abspath(path.join(dir_path, "dimensions/main.js"))], stdin=PIPE, stdout=PIPE, stderr=PIPE
            )
        except FileNotFoundError:
            import warnings

            warnings.warn("Node not installed")
            return state

        # following 4 lines from https://stackoverflow.com/questions/375427/a-non-blocking-read-on-a-subprocess-pipe-in-python
        q = Queue()
        t = Thread(target=enqueue_output, args=(dimension_process.stdout, q))
        t.daemon = True  # thread dies with the program
        t.start()
        atexit.register(cleanup_dimensions)

    # filter out actions such as debug annotations so they aren't saved
    filter_actions(state, env)

    ### 1.2: Initialize a blank state game if new episode is starting ###
    if env.done:
        # TODO: allow resetting to a specific state
        # print("Initialize game", "steps", len(env.steps), "prev_step", prev_step)
        # last_state = None
        # if prev_step >= len(env.steps):
        #     last_state = env.steps[-1]
        # prev_step = len(env.steps)
        # print("prev_step now", prev_step)
        if "seed" in env.configuration:
            seed = env.configuration["seed"]
        else:
            seed = math.floor(random.random() * 1e9)
            env.configuration["seed"] = seed
        if "loglevel" in env.configuration:
            loglevel = env.configuration["loglevel"]
        else:
            loglevel = 0  # warnings, 1: errors, 0: none
            env.configuration["loglevel"] = loglevel
        if "annotations" in env.configuration:
            annotations = env.configuration["annotations"]
        else:
            annotations = False  # warnings, 1: errors, 0: none
            env.configuration["annotations"] = annotations

        if "width" in env.configuration:
            width = env.configuration["width"]
        else:
            width = -1  # -1 for randomly selected
            env.configuration["width"] = width
        if "height" in env.configuration:
            height = env.configuration["height"]
        else:
            height = -1  # -1 for randomly selected
            env.configuration["height"] = height

        initiate = {
            "type": "start",
            "agent_names": [],  # unsure if this is provided?
            "config": env.configuration,
        }
        # if last_state is not None:
        #     initiate["state"] = last_state
        dimension_process.stdin.write((json.dumps(initiate) + "\n").encode())
        dimension_process.stdin.flush()

        agent1res = get_message(dimension_process)
        agent2res = get_message(dimension_process)
        match_obs_meta = get_message(dimension_process)

        player1.observation.player = 0
        player2.observation.player = 1
        player1.observation.updates = agent1res

        # player2.observation.updates = agent2res # duplicated and not added
        player1.observation.globalCityIDCount = match_obs_meta["globalCityIDCount"]
        player1.observation.globalUnitIDCount = match_obs_meta["globalUnitIDCount"]
        player1.observation.width = match_obs_meta["width"]
        player1.observation.height = match_obs_meta["height"]

        game_state = Game()
        game_state._initialize(agent1res)

        return state
    # print("prev_step", prev_step, "stored steps", len(env.steps))
    # prev_step += 1

    ### 2. : Pass in actions (json representation along with id of who made that action), agent information (id, status) to dimensions via stdin
    dimension_process.stdin.write((json.dumps(state) + "\n").encode())
    dimension_process.stdin.flush()

    ### 3.1 : Receive and parse the observations returned by dimensions via stdout
    agent1res = json.loads(dimension_process.stderr.readline())
    agent2res = json.loads(dimension_process.stderr.readline())
    game_state._update(agent1res)

    # receive meta info such as global ID and map sizes for purposes of being able to start from specific state
    match_obs_meta = json.loads(dimension_process.stderr.readline())
    match_status = json.loads(dimension_process.stderr.readline())

    while True:
        try:
            line = q.get_nowait()
        except Empty:
            # no standard error received, break
            break
        else:
            # standard error output received, print it out
            print(line.decode(), file=sys.stderr, end="")

    ### 3.2 : Send observations to each agent through here. Like dimensions, first observation can include initialization stuff, then we do the looping

    player1.observation.updates = agent1res

    player1.observation.globalCityIDCount = match_obs_meta["globalCityIDCount"]
    player1.observation.globalUnitIDCount = match_obs_meta["globalUnitIDCount"]
    player1.observation.width = match_obs_meta["width"]
    player1.observation.height = match_obs_meta["height"]
    # player2.observation.updates = agent2res # duplicated and not added

    player1.observation.player = 0
    player2.observation.player = 1

    ### 3.3 : handle rewards
    # reward here is defined as the sum of number of city tiles
    player1.reward = compute_reward(game_state.players[0])
    player2.reward = compute_reward(game_state.players[1])
    player1.observation.reward = int(player1.reward)
    player2.observation.reward = int(player2.reward)

    ### 3.4 Handle finished match status
    if match_status["status"] == "finished":
        if player1.status == "ACTIVE":
            player1.status = "DONE"
        if player2.status == "ACTIVE":
            player2.status = "DONE"
    return state


def interpreter(state, env):
    try:
        from luxai_s3.wrappers import LuxAIS3GymEnv, RecordEpisode

        global luxenv, prev_obs, state_obs, default_env_cfg
        player_0 = state[0]
        player_1 = state[1]
        # filter out actions such as debug annotations so they aren't saved
        # filter_actions(state, env)

        if env.done:
            if "seed" in env.configuration:
                seed = int(env.configuration["seed"])
            else:
                seed = math.floor(random.random() * 1e9)
                env.configuration["seed"] = seed

            luxenv = LuxAIS3GymEnv(numpy_output=True)
            luxenv = RecordEpisode(luxenv, save_on_close=False, save_on_reset=False)
            obs, info = luxenv.reset(seed=seed)

            env_cfg_json = info["params"]

            env.configuration.env_cfg = env_cfg_json

            player_0.observation.player = "player_0"
            player_1.observation.player = "player_1"
            player_0.observation.obs = json.dumps(to_json(obs["player_0"]))
            player_1.observation.obs = json.dumps(to_json(obs["player_1"]))

            replay_frame = luxenv.serialize_episode_data(
                dict(
                    states=[luxenv.episode["states"][-1]],
                    metadata=luxenv.episode["metadata"],
                    params=luxenv.episode["params"],
                )
            )
            # don't need to keep metadata/params beyond first step
            player_0.info = dict(replay=replay_frame)
            return state

        # validate actions
        player_0_valid_action = True
        player_1_valid_action = True

        def validate_action(action):
            valid = True
            if action.shape != (luxenv.action_space["player_0"].shape):
                valid = False
            return valid

        try:
            player_0_action = np.array(player_0.action["action"])
            assert validate_action(player_0_action)
        except:
            player_0_valid_action = False
            player_0_action = luxenv.action_space.sample()["player_0"] * 0

        try:
            player_1_action = np.array(player_1.action["action"])
            assert validate_action(player_1_action)
        except:
            player_1_valid_action = False
            player_1_action = luxenv.action_space.sample()["player_1"] * 0

        new_state_obs, rewards, terminations, truncations, infos = luxenv.step(
            {"player_0": player_0_action, "player_1": player_1_action}
        )

        # cannot store np arrays in replay jsons so must convert to list
        player_0.action = player_0_action.tolist()
        player_1.action = player_1_action.tolist()

        dones = dict()
        for k in terminations:
            dones[k] = terminations[k] | truncations[k]

        player_0.observation.player = "player_0"
        player_1.observation.player = "player_1"

        player_0.observation.obs = json.dumps(to_json(new_state_obs["player_0"]))
        player_1.observation.obs = json.dumps(to_json(new_state_obs["player_1"]))

        player_0.reward = int(rewards["player_0"])
        player_1.reward = int(rewards["player_1"])

        player_0.observation.reward = int(player_0.reward)
        player_1.observation.reward = int(player_1.reward)
        replay_frame = luxenv.serialize_episode_data(
            dict(
                states=[luxenv.episode["states"][-1]],
                actions=[luxenv.episode["actions"][-1]],
                metadata=luxenv.episode["metadata"],
                params=luxenv.episode["params"],
            )
        )
        # don't need to keep metadata/params beyond first step
        del replay_frame["metadata"]
        del replay_frame["params"]
        player_0.info = dict(replay=replay_frame)

        if np.all([dones[k] for k in dones]):
            if player_0.status == "ACTIVE":
                player_0.status = "DONE"
            if player_1.status == "ACTIVE":
                player_1.status = "DONE"
        # if player submits invalid action we need to mark the game as failed.
        if not player_0_valid_action:
            player_0.status = "ERROR"
        if not player_1_valid_action:
            player_1.status = "ERROR"
        return state
    except ModuleNotFoundError as e:
        print(e)
        print("Lux AI S3 Dependencies are missing, interpreter will not work")
    return state


def interpreter(agents, env):
    configuration = Configuration(env.configuration)
    shared_agent = agents[0]
    # Assign shared_agent.observation so that changes that we make to the shared observation are propagated back to the agent state.
    shared_agent.observation = shared_observation = Observation(shared_agent.observation)

    def sample():
        """Obtain a value between 0 and sampleResolution to check against a bandit threshold."""
        return random.randint(0, configuration.sample_resolution)

    if env.done:
        # Initialize thresholds
        shared_observation.last_actions = None
        shared_observation.thresholds = [sample() for _ in range(configuration.bandit_count)]
        return agents

    # Provide actions in the next observation so agents can monitor opponents.
    shared_observation.last_actions = [agent.action for agent in agents]
    thresholds = shared_observation.thresholds

    for agent in agents:
        if (
            agent.action is not None
            and isinstance(agent.action, int)
            and 0 <= agent.action < configuration.bandit_count
        ):
            # If the sample is less than the threshold the agent gains reward, otherwise nothing
            agent.reward += 1 if sample() < thresholds[agent.action] else 0
            agent.observation.reward = agent.reward
        else:
            agent.status = "INVALID"
            agent.reward = -1

    initial_thresholds = env.steps[0][0].observation.thresholds
    action_histogram = kaggle_environments.helpers.histogram(shared_observation.last_actions)

    for index, threshold in enumerate(thresholds):
        # Every time a threshold is selected it is multiplied by (decay_rate) for each agent that selected it.
        # When a threshold is not selected it is reduced by (decay_rate) ^ 0 (i.e. no recovery).
        action_count = action_histogram[index] if index in action_histogram else 0
        update_rate = (configuration.decay_rate) ** action_count
        thresholds[index] = min(threshold * update_rate, initial_thresholds[index])

    active_agents = [agent for agent in agents if agent.status == "ACTIVE" or agent.status == "INACTIVE"]

    if len(active_agents) <= 1:
        for agent in active_agents:
            agent.status = "DONE"

    return agents


def interpreter(
    state: list[utils.Struct],
    env: core.Environment,
    logs: list[dict[str, Any]],
) -> list[utils.Struct]:
    """Updates environment using player responses and returns new observations."""
    kaggle_state = state  # Not to be confused with OpenSpiel state.
    del state

    # TODO(jhtschultz): Test reset behavior. Currently containers are restarted
    # after each episode.
    if env.done:
        return kaggle_state

    # --- Get and maybe initialize game and state on the env object ---
    if not hasattr(env, "os_game"):
        game_string = env.configuration.get("openSpielGameString")
        game_name = env.configuration.get("openSpielGameName")

        # Load base game from string to get its parameters
        base_game = pyspiel.load_game(game_string)
        base_params = base_game.get_parameters()

        # Find user-provided params by comparing config to spec defaults
        config_params = env.configuration.get("openSpielGameParameters", {})
        default_params = env.specification.configuration.openSpielGameParameters.get("default", {})
        user_params = {k: v for k, v in config_params.items() if config_params.get(k) != default_params.get(k)}

        # Deprecated: use openSpielGameParameters.max_num_hands instead
        if env.configuration.get("setNumHands", None):
            warnings.warn(
                "setNumHands is deprecated. Use openSpielGameParameters={'max_num_hands': N} instead.",
                DeprecationWarning,
                stacklevel=2,
            )
            if "repeated_poker" not in game_name:
                raise ValueError(f"setNumHands only supported for repeated_poker, not {game_name}")
            user_params["max_num_hands"] = env.configuration.get("setNumHands")

        # Merge: base params from string, then user params override
        merged_params = {**base_params, **user_params}

        # Load the game with merged parameters
        env.os_game = pyspiel.load_game(game_name, merged_params)

        # Check if a proxy exists for this game and use it instead
        proxy_path = GAMES_DIR / game_name / f"{game_name}_proxy.py"
        if proxy_path.is_file():
            env.os_game = pyspiel.load_game(game_name + "_proxy", env.os_game.get_parameters())

        # Store the resolved game string (after merging parameters)
        env.info["openSpielGameStringResolved"] = str(env.os_game)
    if not hasattr(env, "os_state"):
        env.os_state = env.os_game.new_initial_state()
    if not hasattr(env, "chance_rng"):
        seed = env.configuration.get("seed", None)
        env.chance_rng = np.random.default_rng(seed) if seed is not None else np.random
    if "stateHistory" not in env.info:
        env.info["stateHistory"] = [str(env.os_state)]
    if "actionHistory" not in env.info:
        env.info["actionHistory"] = []
        env.info["moveDurations"] = []
        initial_actions, metadata = _get_initial_actions(env.configuration)
        if env.configuration.get("loadPresetHands", False):
            if env.configuration.get("presetHands"):
                raise ValueError("Cannot provide presetHands when loadPresetHands is True.")
            preset_hands_from_file = _load_preset_hands_from_file(env.configuration)
            env.configuration["presetHands"] = preset_hands_from_file
            env.configuration["_presetHandsLoaded"] = True
        preset_hands = _get_preset_hands(env.configuration)
        env.configuration.pop("_presetHandsLoaded", None)
        if initial_actions:
            env.info["initialActions"] = initial_actions
            env.info["openingMetadata"] = metadata
            for action in initial_actions:
                env.os_state.apply_action(action)
                env.info["actionHistory"].append(str(action))
                env.info["stateHistory"].append(str(env.os_state))
        if preset_hands:
            env.info["presetHands"] = copy.deepcopy(preset_hands)
            env.info["presetHandsState"] = {
                "hands": [tuple(hand) for hand in preset_hands],
                "next_index": [0 for _ in preset_hands],
                "current_hand_index": 0,
            }
    if env.configuration.get("useImage", False):
        env.configuration["imageConfig"] = _get_image_config(env.configuration)

    os_game = env.os_game
    os_state = env.os_state
    num_players = os_game.num_players()

    # TODO(jhtschultz): Test reset behavior.
    is_initial_step = len(env.steps) == 1
    if is_initial_step and os_state.is_terminal():
        env.os_state = os_game.new_initial_state()
        os_state = env.os_state

    # --- Apply agent action ---
    acting_agent = os_state.current_player()
    # Per-player tracking for sequential moves.
    action_submitted: int | None = None
    action_submitted_to_string: str | None = None
    action_applied: int | None = None
    move_duration: float | None = None
    # Per-player tracking for simultaneous moves.
    simul_actions_submitted: list[int | None] = [None] * num_players
    simul_actions_submitted_to_string: list[str | None] = [None] * num_players
    simul_actions_applied: list[int | None] = [None] * num_players
    simul_move_durations: list[float | None] = [None] * num_players
    simul_all_valid = False

    strict_mode = bool(env.configuration.get("strictMode", False))

    if is_initial_step:
        pass
    elif 0 <= acting_agent < num_players:
        if kaggle_state[acting_agent]["status"] != "ACTIVE":
            pass
        elif strict_mode and (
            not isinstance(kaggle_state[acting_agent]["action"], dict)
            or set(kaggle_state[acting_agent]["action"].keys()) != {"submission"}
        ):
            kaggle_state[acting_agent]["status"] = "INVALID"
        else:
            action_submitted = kaggle_state[acting_agent]["action"]["submission"]
            if action_submitted in os_state.legal_actions():
                action_submitted_to_string = os_state.action_to_string(action_submitted)
                os_state.apply_action(action_submitted)
                action_applied = action_submitted
                env.info["actionHistory"].append(str(action_applied))
                env.info["stateHistory"].append(str(os_state))
                # Visualizers (e.g. goTransformer) read actionString off the
                # action dict to render moves. The LLM harness populates this
                # itself; for code-submission agents we populate it here.
                kaggle_state[acting_agent]["action"]["actionString"] = action_submitted_to_string
            elif action_submitted == AGENT_ERROR_ACTION:
                kaggle_state[acting_agent]["status"] = "ERROR"
            else:
                kaggle_state[acting_agent]["status"] = "INVALID"
            try:
                if "duration" in logs[acting_agent]:
                    move_duration = round(logs[acting_agent]["duration"], 3)
                    env.info["moveDurations"].append(move_duration)
                else:
                    env.info["moveDurations"].append(None)
            except Exception:
                pass  # No logs when stepping the env manually.

    elif acting_agent == pyspiel.PlayerId.SIMULTANEOUS:
        # Collect and validate actions from all players. Players with no
        # legal actions (INACTIVE) get kInvalidAction per OpenSpiel convention.
        actions_for_apply: list[int] = [pyspiel.INVALID_ACTION] * num_players
        simul_all_valid = True
        for pid in range(num_players):
            legal = os_state.legal_actions(pid)
            if not legal:
                # Player has no legal actions at this node — skip.
                continue
            if kaggle_state[pid]["status"] != "ACTIVE":
                simul_all_valid = False
                break
            if strict_mode and (
                not isinstance(kaggle_state[pid]["action"], dict)
                or set(kaggle_state[pid]["action"].keys()) != {"submission"}
            ):
                kaggle_state[pid]["status"] = "INVALID"
                simul_all_valid = False
                break
            sub = kaggle_state[pid]["action"]["submission"]
            simul_actions_submitted[pid] = sub
            if sub == AGENT_ERROR_ACTION:
                kaggle_state[pid]["status"] = "ERROR"
                simul_all_valid = False
                break
            elif sub not in legal:
                kaggle_state[pid]["status"] = "INVALID"
                simul_all_valid = False
                break
            # Capture action string BEFORE applying (state will advance).
            simul_actions_submitted_to_string[pid] = os_state.action_to_string(pid, sub)
            actions_for_apply[pid] = sub

        if simul_all_valid:
            os_state.apply_actions(actions_for_apply)
            for pid in range(num_players):
                simul_actions_applied[pid] = simul_actions_submitted[pid]
                # See note above: surface actionString for visualizers.
                if simul_actions_submitted_to_string[pid] is not None:
                    kaggle_state[pid]["action"]["actionString"] = simul_actions_submitted_to_string[pid]
            env.info["actionHistory"].append(str(actions_for_apply))
            env.info["stateHistory"].append(str(os_state))

        # Record move durations for players who submitted actions.
        for pid in range(num_players):
            if simul_actions_submitted[pid] is None:
                continue
            try:
                if "duration" in logs[pid]:
                    simul_move_durations[pid] = round(logs[pid]["duration"], 3)
                    env.info["moveDurations"].append(simul_move_durations[pid])
                else:
                    env.info["moveDurations"].append(None)
            except Exception:
                pass  # No logs when stepping the env manually.
    elif acting_agent == pyspiel.PlayerId.TERMINAL:
        pass
    elif acting_agent == pyspiel.PlayerId.CHANCE:
        raise ValueError("Interpreter should not be called at chance nodes.")
    else:
        raise ValueError(f"Unknown OpenSpiel player ID: {acting_agent}")

    # --- Step chance nodes ---
    while os_state.is_chance_node():
        outcomes, probs = zip(*os_state.chance_outcomes())
        preset_action = _get_preset_chance_action(env, os_state, outcomes)
        if preset_action is not None:
            chance_action = preset_action
        else:
            chance_action = env.chance_rng.choice(outcomes, p=probs)
        os_state.apply_action(chance_action)
        env.info["actionHistory"].append(str(chance_action))
        env.info["stateHistory"].append(str(os_state))

    # --- Update agent states ---
    agent_error = any(kaggle_state[player_id]["status"] in ["TIMEOUT", "ERROR"] for player_id in range(num_players))
    if agent_error:
        _log.info("AGENT ERROR DETECTED")

    invalid_action = any(kaggle_state[player_id]["status"] == "INVALID" for player_id in range(num_players))
    if invalid_action:
        _log.info("INVALID ACTION DETECTED")

    status: str | None = None
    for player_id, agent_state in enumerate(kaggle_state):
        reward = None
        if agent_error and strict_mode:
            # Per-player scoping like every other competition: offender keeps
            # its natural ERROR / TIMEOUT status (core.py will null its reward),
            # others get DONE + winning reward. The kaggleazure open_spiel
            # carveout is gated on UseModelProxy / EnableInternet so non-DONE
            # statuses no longer void the episode in strict-mode competitions.
            if agent_state["status"] in ("TIMEOUT", "ERROR"):
                status = agent_state["status"]
            else:
                reward = -DEFAULT_INVALID_ACTION_REWARD
                status = "DONE"
        elif agent_error:
            # Set all agent statuses to ERROR in order not to score episode. Preserve
            # TIMEOUT which has the same effect.
            if agent_state["status"] == "TIMEOUT":
                status = "TIMEOUT"
            else:
                status = "ERROR"
        elif invalid_action:
            if agent_state["status"] == "INVALID":
                reward = DEFAULT_INVALID_ACTION_REWARD
            else:
                reward = -DEFAULT_INVALID_ACTION_REWARD
            status = "DONE"
        elif os_state.is_terminal():
            status = "DONE"
            reward = os_state.returns()[player_id]
        elif os_state.is_simultaneous_node():
            if os_state.legal_actions(player_id):
                status = "ACTIVE"
            else:
                status = "INACTIVE"
        elif os_state.current_player() == player_id:
            status = "ACTIVE"
            if not os_state.legal_actions(player_id):
                raise ValueError(f"Active agent {player_id} has no legal actions in state {os_state}.")
        else:
            status = "INACTIVE"
        assert status is not None

        info_dict = {}
        if acting_agent == pyspiel.PlayerId.SIMULTANEOUS:
            info_dict["actionSubmitted"] = simul_actions_submitted[player_id]
            info_dict["actionSubmittedToString"] = simul_actions_submitted_to_string[player_id]
            info_dict["actionApplied"] = simul_actions_applied[player_id]
            info_dict["timeTaken"] = simul_move_durations[player_id]
            info_dict["agentSelfReportedStatus"] = (
                kaggle_state[player_id]["action"].get("status") if kaggle_state[player_id]["action"] else "unknown"
            )
        elif acting_agent == player_id:
            info_dict["actionSubmitted"] = action_submitted
            info_dict["actionSubmittedToString"] = action_submitted_to_string
            info_dict["actionApplied"] = action_applied
            info_dict["timeTaken"] = move_duration
            info_dict["agentSelfReportedStatus"] = (
                kaggle_state[acting_agent]["action"].get("status")
                if kaggle_state[acting_agent]["action"]
                else "unknown"
            )

        # Get observation string based on game's observation type
        if env.configuration.get("observationType") == "information_state":
            obs_string = os_state.information_state_string(player_id)
        else:
            obs_string = os_state.observation_string(player_id)

        obs_update_dict = {
            "observationString": obs_string,
            "currentPlayer": os_state.current_player(),
            "playerId": player_id,
            "isTerminal": os_state.is_terminal(),
            "serializedGameAndState": pyspiel.serialize_game_and_state(os_game, os_state),
        }
        if env.configuration.get("includeLegalActions", False):
            obs_update_dict["legalActions"] = os_state.legal_actions(player_id)
            obs_update_dict["legalActionStrings"] = [
                os_state.action_to_string(action) for action in os_state.legal_actions(player_id)
            ]
        if "imageConfig" in env.configuration:
            obs_update_dict["imageConfig"] = env.configuration["imageConfig"]

        # Apply updates
        for k, v in obs_update_dict.items():
            setattr(agent_state.observation, k, v)
        agent_state["reward"] = reward
        agent_state["info"] = info_dict
        agent_state["status"] = status

    return kaggle_state


def interpreter(state, env):
    configuration = env.configuration
    num_agents = len(state)
    obs0 = state[0].observation

    # Initialize game state if not already done. Run this BEFORE the
    # `env.done` early-return so initialization happens during env.reset()
    # (when all agents are temporarily INACTIVE / "done"). That guarantees
    # the seed is scrubbed from configuration before the first agent.act()
    # call — otherwise agents would see the seed on turn 0.
    if not hasattr(obs0, "planets") or not obs0.planets:
        # Agents must not be able to reconstruct the comet schedule, so
        # resolve_episode_seed scrubs the seed from configuration before the
        # first agent.act() call and stashes it on env.info for the replay.
        seed = resolve_episode_seed(env)
        init_rng = random.Random(seed)

        angular_velocity = init_rng.uniform(0.025, 0.05)
        obs0.angular_velocity = angular_velocity
        obs0.planets = generate_planets(init_rng)
        obs0.initial_planets = [p.copy() for p in obs0.planets]
        obs0.fleets = []
        obs0.next_fleet_id = 0
        obs0.comets = []
        obs0.comet_planet_ids = []

        # Assign home planets — pick a random symmetric group of 4. Under
        # 4-fold rotational symmetry, every group's 4 copies are 90°
        # rotations of each other, so any group is fair for both 2p and 4p.
        num_groups = len(obs0.planets) // 4
        if num_groups > 0:
            home_group = init_rng.randint(0, num_groups - 1)
            base = home_group * 4

            if num_agents == 2:
                obs0.planets[base][1] = 0  # Q1
                obs0.planets[base][5] = 10
                obs0.planets[base + 3][1] = 1  # Q4
                obs0.planets[base + 3][5] = 10
            elif num_agents == 4:
                for j in range(4):
                    obs0.planets[base + j][1] = j
                    obs0.planets[base + j][5] = 10

        for i in range(num_agents):
            state[i].observation.player = i
            if i > 0:
                state[i].observation.angular_velocity = obs0.angular_velocity
                state[i].observation.planets = obs0.planets
                state[i].observation.initial_planets = obs0.initial_planets
                state[i].observation.fleets = obs0.fleets
                state[i].observation.next_fleet_id = obs0.next_fleet_id
                state[i].observation.comets = obs0.comets
                state[i].observation.comet_planet_ids = obs0.comet_planet_ids

        return state

    if env.done:
        return state

    # Remove expired comets before fleet launch so agents can't act on them
    expired_comet_pids = []
    for group in obs0.comets:
        idx = group["path_index"]
        for i, pid in enumerate(group["planet_ids"]):
            if idx >= len(group["paths"][i]):
                expired_comet_pids.append(pid)
    if expired_comet_pids:
        expired_set = set(expired_comet_pids)
        obs0.planets = [p for p in obs0.planets if p[0] not in expired_set]
        obs0.initial_planets = [
            p for p in obs0.initial_planets if p[0] not in expired_set
        ]
        obs0.comet_planet_ids = [
            pid for pid in obs0.comet_planet_ids if pid not in expired_set
        ]
        for group in obs0.comets:
            group["planet_ids"] = [
                pid for pid in group["planet_ids"] if pid not in expired_set
            ]
        obs0.comets = [g for g in obs0.comets if g["planet_ids"]]

    # Spawn extra-solar comets at designated steps
    step = get(obs0, "step", 0)
    comet_speed = configuration.cometSpeed
    if (step + 1) in COMET_SPAWN_STEPS:
        # Derive a per-spawn RNG from the episode seed so comet shape and
        # ship counts are reproducible. Seed lives on env.info to keep it
        # hidden from agents (see init block above).
        env_info = getattr(env, "info", None) or {}
        episode_seed = env_info.get("seed", 0) or 0
        comet_rng = random.Random(f"orbit_wars-comet-{episode_seed}-{step + 1}")
        comet_paths = generate_comet_paths(
            obs0.initial_planets,
            obs0.angular_velocity,
            step + 1,
            obs0.comet_planet_ids,
            comet_speed,
            rng=comet_rng,
        )
        if comet_paths:
            next_id = max(p[0] for p in obs0.planets) + 1
            comet_ships = min(
                comet_rng.randint(1, 99),
                comet_rng.randint(1, 99),
                comet_rng.randint(1, 99),
                comet_rng.randint(1, 99),
            )
            group = {"planet_ids": [], "paths": comet_paths, "path_index": -1}
            for i, p_path in enumerate(comet_paths):
                pid = next_id + i
                group["planet_ids"].append(pid)
                obs0.comet_planet_ids.append(pid)
                # Start off-board; first advancement will place at path[0]
                planet = [
                    pid,
                    -1,
                    -99,
                    -99,
                    COMET_RADIUS,
                    comet_ships,
                    COMET_PRODUCTION,
                ]
                obs0.planets.append(planet)
                obs0.initial_planets.append(planet[:])
            obs0.comets.append(group)

    # 0. Fleet Launch
    def process_moves(player_id, action):
        if not action or not isinstance(action, list):
            return
        for move in action:
            if len(move) != 3:
                continue
            from_id, angle, ships = move
            ships = int(ships)  # Sanitize to integer

            from_planet = next((p for p in obs0.planets if p[0] == from_id), None)

            if from_planet and from_planet[1] == player_id:
                if from_planet[5] >= ships and ships > 0:
                    from_planet[5] -= ships
                    # Start fleet just outside the planet so it doesn't
                    # immediately collide with its origin.
                    start_x = from_planet[2] + math.cos(angle) * (from_planet[4] + 0.1)
                    start_y = from_planet[3] + math.sin(angle) * (from_planet[4] + 0.1)
                    obs0.fleets.append(
                        [
                            obs0.next_fleet_id,
                            player_id,
                            start_x,
                            start_y,
                            angle,
                            from_id,
                            ships,
                        ]
                    )
                    obs0.next_fleet_id += 1

    for i in range(num_agents):
        process_moves(i, state[i].action)

    # 1. Production
    for planet in obs0.planets:
        if planet[1] != -1:
            planet[5] += planet[6]

    # 2. Compute each planet's end-of-tick position up front, so fleet
    # movement can use a swept-pair (continuous) check that accounts for
    # both objects moving in the same tick.
    angular_velocity = obs0.angular_velocity
    step = get(obs0, "step", 1)
    comet_pid_set = set(obs0.comet_planet_ids)
    initial_by_id = {p[0]: p for p in obs0.initial_planets}

    # planet_paths: pid -> (old_pos, new_pos, check_collision)
    # check_collision=False means the planet appears mid-tick (first comet
    # placement) and shouldn't be tested against fleets this tick.
    planet_paths = {}
    expired_comet_pids = []

    for planet in obs0.planets:
        if planet[0] in comet_pid_set:
            continue
        old_pos = (planet[2], planet[3])
        new_pos = old_pos
        initial_p = initial_by_id.get(planet[0])
        if initial_p is not None:
            dx = initial_p[2] - CENTER
            dy = initial_p[3] - CENTER
            r = math.sqrt(dx ** 2 + dy ** 2)
            if r + planet[4] < ROTATION_RADIUS_LIMIT:
                initial_angle = math.atan2(dy, dx)
                current_angle = initial_angle + angular_velocity * step
                new_pos = (
                    CENTER + r * math.cos(current_angle),
                    CENTER + r * math.sin(current_angle),
                )
        planet_paths[planet[0]] = (old_pos, new_pos, True)

    for group in obs0.comets:
        group["path_index"] += 1
        idx = group["path_index"]
        for i, pid in enumerate(group["planet_ids"]):
            planet = next((p for p in obs0.planets if p[0] == pid), None)
            if planet is None:
                continue
            p_path = group["paths"][i]
            old_pos = (planet[2], planet[3])
            if idx >= len(p_path):
                expired_comet_pids.append(pid)
                # Comet stays put this tick; remove after combat.
                planet_paths[pid] = (old_pos, old_pos, True)
            else:
                new_pos = (p_path[idx][0], p_path[idx][1])
                # First placement uses an off-board placeholder for old_pos.
                check = old_pos[0] >= 0
                planet_paths[pid] = (old_pos, new_pos, check)

    # 3. Fleet Movement (with continuous swept-pair collision detection)
    # Speed scales with fleet size: 1 ship = 1/turn, max = shipSpeed (default 6)
    max_speed = configuration.shipSpeed
    fleets_to_remove = []
    combat_lists = {p[0]: [] for p in obs0.planets}

    for fleet in obs0.fleets:
        angle = fleet[4]
        ships = fleet[6]
        speed = 1.0 + (max_speed - 1.0) * (math.log(ships) / math.log(1000)) ** 1.5
        speed = min(speed, max_speed)
        old_pos = (fleet[2], fleet[3])
        fleet[2] += math.cos(angle) * speed
        fleet[3] += math.sin(angle) * speed
        new_pos = (fleet[2], fleet[3])

        # Check if fleet path intersected any planet (continuous collision).
        # Check planets first so fast fleets that would overshoot the bounds
        # or sun still get credit for hitting a planet along the way.
        hit_planet = False
        for planet in obs0.planets:
            path = planet_paths.get(planet[0])
            if path is None or not path[2]:
                continue
            p_old, p_new, _ = path
            if swept_pair_hit(old_pos, new_pos, p_old, p_new, planet[4]):
                combat_lists[planet[0]].append(fleet)
                fleets_to_remove.append(fleet)
                hit_planet = True
                break
        if hit_planet:
            continue

        # Check if fleet went out of bounds
        if not (0 <= fleet[2] <= BOARD_SIZE and 0 <= fleet[3] <= BOARD_SIZE):
            fleets_to_remove.append(fleet)
            continue

        # Check if fleet path crossed the sun
        if point_to_segment_distance((CENTER, CENTER), old_pos, new_pos) < SUN_RADIUS:
            fleets_to_remove.append(fleet)
            continue

    # 4. Apply planet movement (collisions were already resolved above).
    for planet in obs0.planets:
        path = planet_paths.get(planet[0])
        if path is not None:
            planet[2], planet[3] = path[1]

    # Remove expired comets immediately
    if expired_comet_pids:
        expired_set = set(expired_comet_pids)
        obs0.planets = [p for p in obs0.planets if p[0] not in expired_set]
        obs0.initial_planets = [
            p for p in obs0.initial_planets if p[0] not in expired_set
        ]
        obs0.comet_planet_ids = [
            pid for pid in obs0.comet_planet_ids if pid not in expired_set
        ]
        for group in obs0.comets:
            group["planet_ids"] = [
                pid for pid in group["planet_ids"] if pid not in expired_set
            ]
        obs0.comets = [g for g in obs0.comets if g["planet_ids"]]

    obs0.fleets = [f for f in obs0.fleets if f not in fleets_to_remove]

    # 5. Combat Resolution
    for pid, planet_fleets in combat_lists.items():
        planet = next((p for p in obs0.planets if p[0] == pid), None)
        if not planet or not planet_fleets:
            continue

        # Sum ships per player
        player_ships = {}
        for fleet in planet_fleets:
            owner = fleet[1]
            player_ships[owner] = player_ships.get(owner, 0) + fleet[6]

        if not player_ships:
            continue

        sorted_players = sorted(
            player_ships.items(), key=lambda item: item[1], reverse=True
        )
        top_player, top_ships = sorted_players[0]

        if len(sorted_players) > 1:
            second_ships = sorted_players[1][1]
            survivor_ships = top_ships - second_ships

            if sorted_players[0][1] == sorted_players[1][1]:
                survivor_ships = 0

            survivor_owner = top_player if survivor_ships > 0 else -1
        else:
            survivor_owner = top_player
            survivor_ships = top_ships

        if survivor_ships > 0:
            if planet[1] == survivor_owner:
                planet[5] += survivor_ships
            else:
                planet[5] -= survivor_ships
                if planet[5] < 0:
                    planet[1] = survivor_owner
                    planet[5] = abs(planet[5])

    for i in range(1, num_agents):
        state[i].observation.planets = obs0.planets
        state[i].observation.initial_planets = obs0.initial_planets
        state[i].observation.fleets = obs0.fleets
        state[i].observation.next_fleet_id = obs0.next_fleet_id
        state[i].observation.comets = obs0.comets
        state[i].observation.comet_planet_ids = obs0.comet_planet_ids

    terminated = False
    step = get(obs0, "step", 0)
    if step >= configuration.episodeSteps - 2:
        terminated = True

    alive_players = set()
    for p in obs0.planets:
        if p[1] != -1:
            alive_players.add(p[1])
    for f in obs0.fleets:
        alive_players.add(f[1])

    if len(alive_players) <= 1:
        terminated = True

    if terminated:
        for s in state:
            s.status = "DONE"

        scores = [0] * num_agents
        for p in obs0.planets:
            if p[1] != -1:
                scores[p[1]] += p[5]
        for f in obs0.fleets:
            scores[f[1]] += f[6]

        max_score = max(scores)
        for i in range(num_agents):
            if scores[i] == max_score and max_score > 0:
                state[i].reward = 1
            else:
                state[i].reward = -1

    return state


def interpreter(state, env):
    configuration = env.configuration
    obs0 = state[0].observation

    # ---- Init (env.reset). Done before the env.done early-return so it
    # runs even though agents are temporarily INACTIVE at reset.
    if not _get(obs0, "planets", None):
        if not hasattr(env, "info") or env.info is None:
            env.info = {}
        seed = env.info.get("seed")
        if seed is None:
            seed = _get(configuration, "seed", None)
        if seed is None:
            seed = random.randrange(2**31)
        # Publish the resolved seed: env.info for the replay, and back into
        # configuration so replaying with the same configuration is exactly
        # reproducible. NOT scrubbed — the map is fully observable.
        env.info["seed"] = seed
        try:
            configuration.seed = seed
        except (AttributeError, TypeError):
            configuration["seed"] = seed

        map_text = _get(configuration, "map", "random")
        if map_text is None or map_text == "random":
            planets, fleets = generate_map(seed)
        elif isinstance(map_text, str) and map_text.lstrip().startswith("P "):
            planets, fleets = parse_map(map_text)
        else:
            raise ValueError(f"configuration.map must be 'random' or a map text starting with 'P '; got {map_text!r}")

        _broadcast(state, planets, fleets)
        # `player` is per-agent and is initialised from the spec defaults
        # ([1, 2]); we don't need to set it manually here.
        return state

    if env.done:
        return state

    planets = obs0.planets
    fleets = obs0.fleets

    # ---- Validate both players' actions against the original ExecuteOrder
    # checks. Bad orders forfeit the game. core.py may have already marked
    # an agent TIMEOUT/ERROR/INVALID (with action=None) before calling us;
    # treat those as forfeits too rather than letting _validate_orders(None)
    # pass and silently freezing that player for the rest of the episode.
    actions = [_get(state[i], "action", []) for i in range(len(state))]
    prior_bad = [_get(state[i], "status", "ACTIVE") in ("TIMEOUT", "ERROR", "INVALID") for i in range(len(state))]
    valid = [
        not prior_bad[i] and _validate_orders(actions[i], planets, state[i].observation.player)
        for i in range(len(state))
    ]

    if not valid[0] or not valid[1]:
        # Still apply the valid player's orders and advance one tick so the
        # final recorded frame reflects ship growth and fleet arrivals for
        # this turn — otherwise visualizers show fleets stuck mid-flight.
        for i in range(len(state)):
            if valid[i]:
                _apply_orders(actions[i], planets, fleets, state[i].observation.player)
        _do_time_step(planets, fleets)
        _broadcast(state, planets, fleets)
        for i, ok in enumerate(valid):
            if not ok:
                # Preserve TIMEOUT / ERROR from core.py; otherwise INVALID.
                if _get(state[i], "status", "ACTIVE") not in ("TIMEOUT", "ERROR"):
                    state[i].status = "INVALID"
                state[i].reward = None
            else:
                state[i].status = "DONE"
                state[i].reward = 1
        return state

    # ---- Apply orders (player 1 then player 2), advance one tick, then
    # check the winner conditions in the same order as Game::Winner.
    for i in range(len(state)):
        _apply_orders(actions[i], planets, fleets, state[i].observation.player)

    _do_time_step(planets, fleets)
    _broadcast(state, planets, fleets)

    alive = _alive_players(planets, fleets)
    step = _get(obs0, "step", 0)
    # obs.step is the previous state's step; core.py bumps it to len(steps)
    # after we return. So `step + 2 >= episodeSteps` detects the final call.
    max_turns_reached = step + 2 >= configuration.episodeSteps

    terminated = False
    if len(alive) <= 1 or max_turns_reached:
        terminated = True

    if terminated:
        for s in state:
            s.status = "DONE"
        if len(alive) == 1:
            winner = next(iter(alive))
            for s in state:
                s.reward = 1 if s.observation.player == winner else -1
        elif len(alive) == 0:
            for s in state:
                s.reward = 0
        else:
            scores = {s.observation.player: _total_ships(planets, fleets, s.observation.player) for s in state}
            top = max(scores.values())
            tied = sum(1 for v in scores.values() if v == top)
            if tied > 1:
                for s in state:
                    s.reward = 0
            else:
                for s in state:
                    s.reward = 1 if scores[s.observation.player] == top else -1

    return state


def interpreter(state, env):
    """
    Core game logic. Called once per step by the kaggle-environments engine.

    On the first call (``env.done == True``), this initialises the game.
    On subsequent calls it processes the active agent's actions, checks
    win/draw conditions, updates observations, and swaps the active player.

    Args:
        state: list of per-agent state structs. Each has:
            .action        - the action returned by the agent
            .reward        - read/write reward
            .status        - ACTIVE / INACTIVE / DONE / ERROR / INVALID / TIMEOUT
            .observation   - per-agent observation struct
        env: environment handle with:
            .configuration - merged configuration struct
            .done          - True on the initialisation call
            .steps         - list of all previous steps

    Returns:
        state (modified in-place)
    """
    key = id(env)

    # ------------------------------------------------------------------
    # Initialisation (first call after env.reset)
    # ------------------------------------------------------------------
    if env.done:
        return _interpreter_init(state, env, key)

    game = _games.get(key)
    if game is None:
        for agent in state:
            agent.status = "ERROR"
        return state

    # ------------------------------------------------------------------
    # Determine which agent is active
    # ------------------------------------------------------------------
    active_idx = _get_active_index(state)
    if active_idx is None:
        return state  # both done / error

    # ------------------------------------------------------------------
    # Execute agent actions, end turn, check outcomes
    # ------------------------------------------------------------------
    _process_turn(state, env, game, active_idx, key)

    return state


def interpreter(state, env):
    player1 = state[0]
    player2 = state[1]

    # Specification can fully handle the reset.
    if env.done:
        return state

    def is_valid_action(player, sign_count):
        return player.action is not None and isinstance(player.action, int) and 0 <= player.action < sign_count

    # Check for validity of actions
    is_player1_valid = is_valid_action(player1, env.configuration.signs)
    is_player2_valid = is_valid_action(player2, env.configuration.signs)
    if not is_player2_valid:
        player2.status = "INVALID"
        player2.reward = 0

        if is_player1_valid:
            player1.status = "DONE"
            player1.reward = 1
            return state

    if not is_player1_valid:
        player1.status = "INVALID"
        player1.reward = 0

        if is_player2_valid:
            player2.status = "DONE"
            player2.reward = 1
            return state
        else:
            return state

    score = get_score(player1.action, player2.action)
    player1.observation.lastOpponentAction = player2.action
    player1.reward += score
    player2.observation.lastOpponentAction = player1.action
    player2.reward -= score
    player1.observation.reward = int(player1.reward)
    player2.observation.reward = int(player2.reward)
    remaining_steps = env.configuration.episodeSteps - player1.observation.step - 1

    # This is the last step
    if remaining_steps <= 1:
        player1.status = "DONE"
        player2.status = "DONE"
        # Player performance too similar, consider the match a tie.
        if abs(player1.reward) < env.configuration.tieRewardThreshold:
            player1.reward = 0
            player2.reward = 0
    return state


def interpreter(state, env):
    """
    * Required interface function for kaggle environments package *

    This is the primary interface for the kaggle environment (kEnv) to step game forward.
    Briefly flow of logic is:
    Initialization - kEnv creates werewolf object and chooses players. Schema definition for
    this is in werewolf.json
    1) kEnv calls interpreter() with current game state recorded in env.game_state
    2) interpreter() reads game state and any new player actions and updates
       the games state based on those actions and flow of the game to env.game_state.
    3) interpreter() writes events to history data and also writes events about
       state change in the game to env.game_state and returns back to kEnv
    4) kEnv parses out the relevant game events via agent logic in harness/base.py,
       constructs final prompt, and performs external API calls for models and records back
       to env.game_state
    Go back to 1 and continue

    For example - consider discussion and voting by villagers. werewolf.interpreter()
    updates phase and writes history entry that solicits players for discussion.
    kEnv calls agents to get their discussion and writes them to the history/game state.
    kEnv then calls interpreter() that then updates game phase and writes history entry soliciting
    votes for exile. kEnv then calls agents and associated models to get their votes and writes
    responses to game state. env then calls interpreter() and moderator collects votes, determine
    who was exiled, performs that action and advances game phase and game state.
    And so on...

    Note - The UI is also updated after each call to interpreter() as that is the tick unit
    for the game.

    Note - env framework assumes that there is an action to be done by player, but
    for werewolf there are places where moderator is the one taking the action (e.g.
    counting votes and performing exile) so some game 'ticks' are larger than others.

    state: list of dictionaries, one for each agent.
           Each dict has: {observation, action, reward, status, info}
    env:   the kaggle_environments.Environment object itself including the env.game_state
    """
    agent_error = False
    for status_code in ["TIMEOUT", "ERROR", "INVALID"]:
        if log_error(status_code, state, env):
            agent_error = True

    # --- Initialize Moderator and GameState if it's the start of an episode ---
    if not hasattr(env, "moderator") or env.done:  # env.done is true after reset by Kaggle core
        initialize_moderator(state, env)

    moderator: Moderator = env.moderator
    game_state: GameState = env.game_state

    # 1. Collect and parse actions from Kaggle agents
    parsed_player_actions = parse_player_actions(state, moderator, game_state)

    # 2. Advance the Moderator
    moderator.advance(parsed_player_actions)

    # 3. Update Kaggle state (observations, rewards, statuses)
    is_game_done = moderator.is_game_over() or agent_error
    current_info = {}
    if is_game_done:
        record_game_end(state, env, game_state, current_info, agent_error)

    # 4. Moderator interprets player actions, updates game phase, and advance game player actions
    active_player_ids_after_advance = set(moderator.get_active_player_ids())

    # 4.1. Accumulate God mode observations from env for rendering
    global_messages = env.game_state.consume_messages()
    global_data = [rec.serialize() for rec in global_messages]
    env.info[EnvInfoKeys.MODERATOR_OBS].append(global_data)

    # 4.2. Update observations for individual agents
    update_agent_messages(
        state, env, moderator, game_state, is_game_done, current_info, active_player_ids_after_advance, agent_error
    )
    return state


def interpreter(state, env):
    # Initialization
    if len(state[0].observation.get("words", [])) == 0:
         initialize_game(state, env.configuration)
         active_player = state[0].observation.current_turn
         for i in range(4):
             state[i].status = "ACTIVE" if i == active_player else "INACTIVE"
         update_visibility(state)
         return state
             
    if env.done:
        return state

    prev_blue_reward = state[0].reward or 0
    prev_yellow_reward = state[2].reward or 0

    process_action(state, env.configuration)
    update_visibility(state)
    
    # Custom Memory Logic
    obs = state[0].observation
    games_per_episode = env.configuration.get("games_per_episode", 1)
    
    # Always track turns within the current game for all agents
    for s in state:
        track_turn(s.observation, state)
    
    if games_per_episode > 1:
        is_done = all(s.status in ["DONE", "INVALID"] for s in state)
        if is_done:
            winner = None
            if (state[0].reward or 0) > prev_blue_reward: winner = "blue"
            elif (state[2].reward or 0) > prev_yellow_reward: winner = "yellow"
            
            # Update wins in observation
            if winner == "blue":
                for s in state:
                    s.observation.blue_wins += 1
            elif winner == "yellow":
                for s in state:
                    s.observation.yellow_wins += 1
            
            window_size = env.configuration.get("memory_window_size", 0)
            # Per-game memory lives on every agent's observation (track_turn
            # writes to all four), so save/reset must touch all of them — not
            # just state[0] — or subsequent prompts will leak prior-game turns.
            for s in state:
                save_game_to_history(s.observation, winner, window_size)

            if obs.current_game + 1 < games_per_episode:
                for s in state:
                    s.observation.current_game += 1
                    s.observation.current_game_turns = []
                    s.observation._last_clue = ""
                    s.observation._last_revealed = [False] * len(s.observation.revealed)

                # Reset board (re-init)
                initialize_game(state, env.configuration)

                # initialize_game writes full roles to every agent; mask them
                # again for the guessers before the new game's snapshot is
                # returned, mirroring the first-game init path.
                update_visibility(state)

                # Reset agent statuses based on new current_turn
                for i in range(4):
                    state[i].status = "ACTIVE" if i == state[0].observation.current_turn else "INACTIVE"
                    
    return state

