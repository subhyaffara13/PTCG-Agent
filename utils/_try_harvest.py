
def _try_harvest(farm, fx, fy, day):
    tile = farm["tiles"][fy][fx]
    if tile is None:
        return None
    crop = CROPS[tile["crop"]]
    age_days = day - tile["planted_day"]
    if age_days < crop["first_yield_day"]:
        return None

    if crop["ongoing"]:
        # Ongoing plant: take all ready units. The plant is left standing --
        # it may still produce more, or decay may eventually remove it.
        units = tile["yield_units"]
        if units <= 0:
            return None
        tile["yield_units"] = 0
        return (tile["crop"], units)

    # One-time crop: yield_units accumulated via watering during the bonus
    # window and decayed over time after max lifespan. Tile removed on harvest.
    yield_units = tile["yield_units"]
    crop_name = tile["crop"]
    farm["tiles"][fy][fx] = None
    if yield_units <= 0:
        return None
    return (crop_name, yield_units)

