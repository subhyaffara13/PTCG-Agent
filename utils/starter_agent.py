import math


def starter_agent(obs):
    """Carrot loop: buy seed, plant on the current tile, water, harvest at max_yield_day."""
    farms = obs.get("farms", [])
    player = obs.get("player", 0)
    private = obs.get("private", {}) or {}
    if not farms or player >= len(farms):
        return {"farmer": ["PASS"], "hands": [], "market": []}
    farm = farms[player]
    fx, fy = farm["farmer"]
    tile = farm["tiles"][fy][fx]
    day = obs.get("day", 0)
    seeds = private.get("seeds", {})
    shed = private.get("shed", {})

    market = []
    if shed.get("CARROT", 0) > 0:
        market.append(["SELL", "CARROT", shed["CARROT"]])
    if seeds.get("CARROT", 0) == 0 and farm["money"] >= CROPS["CARROT"]["seed"]:
        market.append(["BUY_SEED", "CARROT", 1])

    farmer = ["PASS"]
    if tile is None and seeds.get("CARROT", 0) > 0:
        farmer = ["PLANT", "CARROT"]
    elif isinstance(tile, dict) and tile.get("kind") == "PLANT" and tile["crop"] == "CARROT":
        age = day - tile["planted_day"]
        if age >= CROPS["CARROT"]["max_yield_day"]:
            farmer = ["HARVEST"]
        elif not tile["watered_today"]:
            farmer = ["WATER"]
    return {"farmer": farmer, "hands": [], "market": market}


def starter_agent(obs):
    """Deterministic carrot loop: buy a carrot seed, plant on the current
    tile, water through the bonus window, harvest at max_yield_day, repeat."""
    farms = obs.get("farms", [])
    player = obs.get("player", 0)
    if not farms or player >= len(farms):
        return {"farmer": ["PASS"], "market": []}
    farm = farms[player]
    fx, fy = farm["farmer"]
    tile = farm["tiles"][fy][fx]
    day = obs.get("day", 0)
    carrot_seeds = farm["seeds"].get("CARROT", 0)
    money = farm["money"]
    carrot = CROPS["CARROT"]

    if tile is None:
        if carrot_seeds > 0:
            return {"farmer": ["PLANT", "CARROT"], "market": []}
        market = []
        if money >= carrot["seed"]:
            market.append(["BUY_SEED", "CARROT", 1])
        return {"farmer": ["PASS"], "market": market}

    if tile["crop"] != "CARROT":
        return {"farmer": ["PASS"], "market": []}

    age_days = day - tile["planted_day"]
    if not tile["watered_today"] and age_days <= carrot["max_yield_day"]:
        return {"farmer": ["WATER"], "market": []}
    if age_days >= carrot["max_yield_day"]:
        return {"farmer": ["HARVEST"], "market": []}
    return {"farmer": ["PASS"], "market": []}


def starter_agent(obs):
    moves = []
    player = obs.get("player", 0)
    planets = [Planet(*p) for p in obs.get("planets", [])]

    # Find static planets (orbital_radius + planet_radius >= ROTATION_RADIUS_LIMIT)
    static_targets = []
    for p in planets:
        orbital_r = math.sqrt((p.x - CENTER) ** 2 + (p.y - CENTER) ** 2)
        if orbital_r + p.radius >= ROTATION_RADIUS_LIMIT and p.owner != player:
            static_targets.append(p)

    my_planets = [p for p in planets if p.owner == player]
    for mp in my_planets:
        if mp.ships <= 0:
            continue
        # Find closest static planet not owned by us
        closest = None
        min_dist = float("inf")
        for t in static_targets:
            dist = math.sqrt((mp.x - t.x) ** 2 + (mp.y - t.y) ** 2)
            if dist < min_dist:
                min_dist = dist
                closest = t

        if closest:
            angle = math.atan2(closest.y - mp.y, closest.x - mp.x)
            ships = mp.ships // 2
            if ships >= 20:
                moves.append([mp.id, angle, ships])

    return moves

