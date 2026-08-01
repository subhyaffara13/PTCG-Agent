
def _daily_refresh(farm, current_day=0, turns_per_day=24):
    """End-of-day plant maintenance. Runs at the end of `current_day`:
    1. Kill plants unwatered for 2+ consecutive days.
    2. For surviving ongoing crops, produce 1 unit if the next day is a
       scheduled production day (and the lifetime cap hasn't been hit).
       When the cap is reached, set max_lifespan_step so decay begins the
       day after.
    3. Reset watered_today for the new day."""
    board_size = len(farm["tiles"])
    next_day = current_day + 1
    for y in range(board_size):
        for x in range(board_size):
            tile = farm["tiles"][y][x]
            if tile is None:
                continue

            if tile["watered_today"]:
                tile["consecutive_unwatered"] = 0
            else:
                tile["consecutive_unwatered"] += 1
            tile["watered_today"] = False
            if tile["consecutive_unwatered"] >= 2:
                farm["tiles"][y][x] = None
                continue

            crop_data = CROPS[tile["crop"]]
            # One-time crops gain yield only via watering during the bonus
            # window (handled in _apply_farmer_action); they have no scheduled
            # daily production, so skip the rest of this loop body.
            if not crop_data["ongoing"]:
                continue
            days_since_first = next_day - tile["planted_day"] - crop_data["first_yield_day"]
            if days_since_first < 0:
                continue
            interval = crop_data["interval"]
            if days_since_first % interval != 0:
                continue
            production_count = days_since_first // interval + 1
            if production_count > crop_data["max_yield"]:
                continue
            tile["yield_units"] += 1
            if production_count == crop_data["max_yield"]:
                tile["max_lifespan_step"] = (next_day + 1) * turns_per_day

