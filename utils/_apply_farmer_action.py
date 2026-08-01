
def _apply_farmer_action(farm, action, board_size, day, turns_per_day=24):
    """Mutates farm in place. Returns (crop, yield_units) for a successful HARVEST,
    None otherwise.

    NOTE: invalid or illegal actions are silently no-ops (not status=INVALID).
    A malformed action will not end the game.
    """
    if not isinstance(action, list) or not action:
        return None
    op = action[0]
    fx, fy = farm["farmer"]

    if op in FARMER_MOVES:
        dx, dy = FARMER_MOVES[op]
        nx, ny = fx + dx, fy + dy
        if 0 <= nx < board_size and 0 <= ny < board_size:
            farm["farmer"] = [nx, ny]
        return None

    if op == "PLANT":
        if len(action) < 2:
            return None
        crop = action[1]
        if crop not in CROPS:
            return None
        if farm["tiles"][fy][fx] is not None:
            return None
        if farm["seeds"].get(crop, 0) <= 0:
            return None
        farm["seeds"][crop] -= 1
        farm["tiles"][fy][fx] = _new_plant(crop, day, turns_per_day)
        return None

    if op == "WATER":
        tile = farm["tiles"][fy][fx]
        if tile is None or tile["watered_today"]:
            return None
        tile["watered_today"] = True
        crop_data = CROPS[tile["crop"]]
        if not crop_data["ongoing"]:
            age_days = day - tile["planted_day"]
            window_start = (crop_data["max_yield_day"] + 1) // 2
            if window_start <= age_days <= crop_data["max_yield_day"]:
                tile["yield_units"] = min(crop_data["max_yield"], tile["yield_units"] + 1)
        return None

    if op == "HARVEST":
        return _try_harvest(farm, fx, fy, day)

    return None

