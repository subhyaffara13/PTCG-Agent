
def _daily_refresh_animals(farm, day):
    board_size = len(farm["tiles"])
    next_day = day + 1
    for y in range(board_size):
        for x in range(board_size):
            tile = farm["tiles"][y][x]
            if not (isinstance(tile, dict) and "animal" in tile):
                continue
            if tile["fed_today"]:
                tile["consecutive_unfed"] = 0
            else:
                tile["consecutive_unfed"] += 1
            if tile["consecutive_unfed"] >= 2:
                # Animal escapes; structure remains.
                farm["tiles"][y][x] = {"kind": ANIMALS[tile["animal"]]["structure"]}
                continue
            a = ANIMALS[tile["animal"]]
            days_since_first = next_day - tile["placed_day"] - a["first_yield_day"]
            if days_since_first >= 0 and days_since_first % a["interval"] == 0:
                base = 1
                # Care bonus only consumed on a fed production day.
                bonus = tile.pop("pending_care_bonus", 0) if tile["fed_today"] else 0
                tile["yield_units"] = min(a["max_held"], tile["yield_units"] + base + bonus)
                tile["pending_care_bonus"] = 0
            if tile["cared_today"] and tile["fed_today"]:
                tile["pending_care_bonus"] = tile.get("pending_care_bonus", 0) + 1
            tile["fertilizer_available"] = True
            tile["fed_today"] = False
            tile["cared_today"] = False

