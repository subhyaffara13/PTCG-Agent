import random

def _end_of_day(state, env, day):
    obs0 = state[0].observation
    cfg = env.configuration
    board_size = int(get(cfg, "boardSize", 10))
    turns_per_day = max(1, int(get(cfg, "turnsPerDay", 24)))
    weed_chance = float(get(cfg, "weedSpawnChance", 0.005))
    shed_cap = int(get(cfg, "shedCapacity", 100))
    shop_interval = max(1, int(get(cfg, "townShopUnlockInterval", 3)))

    # Stable RNG keyed off env.info["seed"] + day so replays reproduce.
    seed = env.info.get("seed", 0)
    rng = random.Random((seed * 1_000_003) ^ day)

    for player_id, farm in enumerate(obs0.farms):
        private = state[player_id].observation.private
        _daily_refresh_plants(farm, day, turns_per_day)
        _daily_refresh_animals(farm, day)
        _spawn_weeds(farm, board_size, weed_chance, rng)
        _drop_inventories_to_shed(private, shed_cap)
        farm["farmer"] = list(_default_spawn(board_size))
        farm["hands"] = []
        farm["hires_today"] = 0
        private["inventories"] = [{}]

    next_day = day + 1
    town = obs0.town
    if next_day > 0 and next_day % shop_interval == 0:
        remaining = [s for s in SHOPS if s not in town["unlocked_shops"]]
        if remaining:
            choice = rng.choice(sorted(remaining))
            town["unlocked_shops"].append(choice)

