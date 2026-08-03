import random
from typing import Any
import math


def random_agent(obs: dict) -> list[int]:
    if obs["select"] == None:
        return deck
    return random.sample(list(range(len(obs["select"]["option"]))), obs["select"]["maxCount"])


def random_agent(obs, config):
    return choice([c for c in range(config.columns) if obs.board[c] == EMPTY])


def random_agent(observation, configuration):
    """Simple agent: builds scouts, moves robots north, collects energy."""
    actions = {}
    my_robots = {}

    if not observation.robots:
        return actions

    for uid, data in observation.robots.items():
        rtype, col, row, energy, owner = data[0], data[1], data[2], data[3], data[4]
        if owner == observation.player:
            my_robots[uid] = {
                "type": rtype,
                "col": col,
                "row": row,
                "energy": energy,
                "move_cooldown": data[5] if len(data) > 5 else 0,
                "build_cooldown": data[7] if len(data) > 7 else 0,
            }

    width = configuration.width

    for uid, robot in my_robots.items():
        rtype = robot["type"]
        col = robot["col"]
        row = robot["row"]
        energy = robot["energy"]

        idx = (row - observation.southBound) * width + col
        w = 0
        if 0 <= idx < len(observation.walls) and observation.walls[idx] != -1:
            w = observation.walls[idx]

        if rtype == 0:  # Factory
            wall_north = w & 1
            worker_count = sum(1 for r in my_robots.values() if r["type"] == 2)
            if wall_north:
                # Wall north — jump over it first
                actions[uid] = "JUMP_NORTH"
            elif robot["energy"] >= configuration.workerCost and worker_count < 1 and robot["build_cooldown"] == 0:
                actions[uid] = "BUILD_WORKER"
            else:
                actions[uid] = "NORTH"
        elif rtype == 2:  # Worker
            if (w & 1) and energy >= configuration.wallRemoveCost:
                # Wall north — knock it down
                actions[uid] = "REMOVE_NORTH"
            elif not (w & 1):
                actions[uid] = "NORTH"
            else:
                passable = []
                if not (w & 2):
                    passable.append("EAST")
                if not (w & 8):
                    passable.append("WEST")
                if not (w & 4):
                    passable.append("SOUTH")
                actions[uid] = choice(passable) if passable else "IDLE"
        else:
            # Scouts/miners: try to move north, fallback to other directions
            passable = []
            if not (w & 1):
                passable.append("NORTH")
            if not (w & 2):
                passable.append("EAST")
            if not (w & 4):
                passable.append("SOUTH")
            if not (w & 8):
                passable.append("WEST")
            if passable:
                if "NORTH" in passable:
                    actions[uid] = "NORTH"
                else:
                    actions[uid] = choice(passable)
            else:
                actions[uid] = "IDLE"

    return actions


def random_agent(board):
    me = board.current_player
    remaining_halite = me.halite
    ships = me.ships
    # randomize ship order
    ships = sample(ships, len(ships))
    for ship in ships:
        if ship.cell.halite > ship.halite and randint(0, 1) == 0:
            # 50% chance to mine
            continue
        if ship.cell.shipyard is None and remaining_halite > board.configuration.convert_cost:
            # 5% chance to convert at any time
            if randint(0, 19) == 0:
                remaining_halite -= board.configuration.convert_cost
                ship.next_action = ShipAction.CONVERT
                continue
            # 50% chance to convert if there are no shipyards
            if randint(0, 1) == 0 and len(me.shipyards) == 0:
                remaining_halite -= board.configuration.convert_cost
                ship.next_action = ShipAction.CONVERT
                continue
        # None represents the chance to do nothing
        ship.next_action = choice(ShipAction.moves())
    shipyards = me.shipyards
    # randomize shipyard order
    shipyards = sample(shipyards, len(shipyards))
    ship_count = len(board.next().current_player.ships)
    for shipyard in shipyards:
        # If there are no ships, always spawn if possible
        if ship_count == 0 and remaining_halite > board.configuration.spawn_cost:
            remaining_halite -= board.configuration.spawn_cost
            shipyard.next_action = ShipyardAction.SPAWN
        # 20% chance to spawn if no ships
        elif randint(0, 4) == 0 and remaining_halite > board.configuration.spawn_cost:
            remaining_halite -= board.configuration.spawn_cost
            shipyard.next_action = ShipyardAction.SPAWN


def random_agent():
    return choice([action for action in Action]).name


def random_agent(obs):
    rng = random.Random()
    farms = obs.get("farms", [])
    player = obs.get("player", 0)
    private = obs.get("private", {}) or {}
    farm = farms[player] if farms and player < len(farms) else None
    if farm is None:
        return {"farmer": ["PASS"], "hands": [], "market": []}

    farmer_ops = ["NORTH", "SOUTH", "EAST", "WEST", "WATER", "HARVEST", "PASS"]
    market = []
    seeds = private.get("seeds", {})

    affordable = [c for c in CROPS if CROPS[c]["seed"] <= farm["money"]]
    if affordable and rng.random() < 0.1:
        market.append(["BUY_SEED", rng.choice(affordable), 1])

    available_seeds = [c for c, n in seeds.items() if n > 0]
    if available_seeds and rng.random() < 0.3:
        farmer = ["PLANT", rng.choice(available_seeds)]
    else:
        farmer = [rng.choice(farmer_ops)]

    hands_actions = [[rng.choice(farmer_ops)] for _ in farm.get("hands", [])]
    return {"farmer": farmer, "hands": hands_actions, "market": market}


def random_agent(obs):
    rng = random.Random()
    farmer_ops = ["NORTH", "SOUTH", "EAST", "WEST", "WATER", "HARVEST", "PASS"]
    market = []
    farms = obs.get("farms", [])
    player = obs.get("player", 0)
    money = farms[player]["money"] if farms and player < len(farms) else 0
    seeds = farms[player]["seeds"] if farms and player < len(farms) else {}

    affordable = [c for c in CROPS if CROPS[c]["seed"] <= money]
    if affordable and rng.random() < 0.1:
        crop = rng.choice(affordable)
        market.append(["BUY_SEED", crop, 1])

    available_seeds = [c for c, n in seeds.items() if n > 0]
    if available_seeds and rng.random() < 0.3:
        farmer = ["PLANT", rng.choice(available_seeds)]
    else:
        farmer = [rng.choice(farmer_ops)]

    return {"farmer": farmer, "market": market}


def random_agent(board):
    me = board.current_player
    remaining_kore = me.kore
    shipyards = me.shipyards
    # randomize shipyard order
    shipyards = sample(shipyards, len(shipyards))
    for shipyard in shipyards:
        # 25% chance to launch a large fleet
        if randint(0, 3) == 0 and shipyard.ship_count > 10:
            dir_str = Direction.random_direction().to_char()
            dir2_str = Direction.random_direction().to_char()
            flight_plan = dir_str + str(randint(1, 10)) + dir2_str
            shipyard.next_action = ShipyardAction.launch_fleet_with_flight_plan(
                min(10, math.floor(shipyard.ship_count / 2)), flight_plan
            )
        # else spawn if possible
        elif remaining_kore > board.configuration.spawn_cost * shipyard.max_spawn:
            remaining_kore -= board.configuration.spawn_cost
            shipyard.next_action = ShipyardAction.spawn_ships(shipyard.max_spawn)
        # else launch a small fleet
        elif shipyard.ship_count >= 2:
            dir_str = Direction.random_direction().to_char()
            shipyard.next_action = ShipyardAction.launch_fleet_with_flight_plan(2, dir_str)


def random_agent(observation, configuration):
    return random.randrange(configuration.banditCount - 1)


def random_agent(
    observation: dict[str, Any],
    configuration: dict[str, Any],
) -> int:
    """A built-in random agent specifically for OpenSpiel environments."""
    legal_actions = observation.get("legalActions")
    if not legal_actions:
        return None
    action = int(random.choice(legal_actions))
    # strictMode requires the action dict to contain ONLY 'submission'.
    if configuration.get("strictMode", False):
        return {"submission": action}
    thoughts = " ".join(random.choices(_RANDOM_THOUGHT_WORDS, k=8))
    return {"submission": action, "thoughts": thoughts}


def random_agent(obs):
    moves = []
    player = obs.get("player", 0)
    planets = [Planet(*p) for p in obs.get("planets", [])]
    for p in planets:
        if p.owner == player and p.ships > 0:
            angle = random.uniform(0, 2 * math.pi)
            ships = p.ships // 2
            if ships >= 20:
                moves.append([p.id, angle, ships])
    return moves


def random_agent(obs, config=None):
    """Each owned planet has a 30% chance of sending half its ships to a
    random other planet."""
    player = _get(obs, "player", 1)
    planets = _get(obs, "planets", []) or []
    moves = []
    if not planets:
        return moves
    for p in planets:
        if p[3] != player or p[4] < 2:
            continue
        if random.random() > 0.3:
            continue
        ships = p[4] // 2
        targets = [t for t in planets if t[0] != p[0]]
        if not targets:
            continue
        target = random.choice(targets)
        moves.append([p[0], target[0], ships])
    return moves


def random_agent(obs):
    raw_obs = get_raw_observation(obs)

    entries = raw_obs.new_player_event_views
    current_phase = DetailedPhase(raw_obs.detailed_phase)
    my_role = raw_obs.role
    all_player_names = raw_obs.all_player_ids
    my_id = raw_obs.player_id
    alive_players = raw_obs.alive_players
    day = raw_obs.day
    phase = raw_obs.game_state_phase
    common_args = {"day": day, "phase": phase, "actor_id": my_id}

    action = NoOpAction(**common_args, reasoning="There's nothing to be done.")  # Default action
    threat_level = random.choice(_PERCEIVED_THREAT_LEVELS)

    if current_phase == DetailedPhase.NIGHT_AWAIT_ACTIONS:
        if my_role == RoleConst.WEREWOLF:
            history_entry = get_last_action_request(entries, EventName.VOTE_REQUEST)
            if history_entry:
                valid_targets = history_entry.data.get("valid_targets")
                if valid_targets:
                    target_id = random.choice(valid_targets)
                    action = VoteAction(
                        **common_args,
                        target_id=target_id,
                        reasoning="I randomly chose one.",
                        perceived_threat_level=threat_level,
                    )

        elif my_role == RoleConst.DOCTOR:
            history_entry = get_last_action_request(entries, EventName.HEAL_REQUEST)
            if history_entry:
                valid_targets = history_entry.data["valid_candidates"]
                if valid_targets:
                    target_id = random.choice(valid_targets)
                    action = HealAction(
                        **common_args,
                        target_id=target_id,
                        reasoning="I randomly chose one to heal.",
                        perceived_threat_level=threat_level,
                    )

        elif my_role == RoleConst.SEER:
            history_entry = get_last_action_request(entries, EventName.INSPECT_REQUEST)
            if history_entry:
                valid_targets = history_entry.data["valid_candidates"]
                if valid_targets:
                    target_id = random.choice(valid_targets)
                    action = InspectAction(
                        **common_args,
                        target_id=target_id,
                        reasoning="I randomly chose one to inspect.",
                        perceived_threat_level=threat_level,
                    )

    elif current_phase in [DetailedPhase.DAY_BIDDING_AWAIT, DetailedPhase.DAY_CHAT_AWAIT]:
        if current_phase == DetailedPhase.DAY_BIDDING_AWAIT:
            if my_id in alive_players:
                action = BidAction(
                    **common_args,
                    amount=random.randint(1, 4),
                    reasoning="I am bidding randomly.",
                    perceived_threat_level=threat_level,
                )
        else:  # It's a chat turn (DAY_CHAT_AWAIT)
            if my_id in alive_players:
                action = ChatAction(
                    **common_args,
                    message=random.choice(
                        [
                            "Hello everyone!",
                            f"I suspect {random.choice(all_player_names)}.",
                            "Any information to share?",
                            "I am a simple Villager just trying to survive.",
                            "Let's think carefully before voting.",
                        ]
                    ),
                    reasoning="I randomly chose one message.",
                    perceived_threat_level=threat_level,
                )

    elif current_phase == DetailedPhase.DAY_VOTING_AWAIT:
        if my_id in alive_players:
            # A real agent would parse the prompt for valid targets
            valid_targets = [p_id for p_id in alive_players if p_id != my_id]
            if valid_targets:
                action = VoteAction(
                    **common_args,
                    target_id=random.choice(valid_targets),
                    reasoning="I randomly chose one.",
                    perceived_threat_level=threat_level,
                )

    return action.serialize()


def random_agent(obs, config):
    if obs.current_turn in [0, 2]:
        return {"clue": "random", "number": 1}
    else:
        valid_guesses = [i for i in range(25) if not obs.revealed[i]]
        if valid_guesses:
            return random.choice(valid_guesses)
        return -1


def random_agent(observation, configuration):
    """
    a blank, completely empty agent, usually incapable of surviving past the first night
    """
    global game_state

    ### Do not edit ###
    if observation["step"] == 0:
        game_state = Game()
        game_state._initialize(observation["updates"])
        game_state._update(observation["updates"][2:])
    else:
        game_state._update(observation["updates"])

    actions = []

    ### AI Code goes down here! ###
    player = game_state.players[observation.player]
    for unit in player.units:
        dirs = [DIRECTIONS.NORTH, DIRECTIONS.WEST, DIRECTIONS.EAST, DIRECTIONS.SOUTH]
        action = unit.move(random.choice(dirs))
        actions.append(action)

    return actions

