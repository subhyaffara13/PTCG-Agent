
def _new_plant(crop, day, turns_per_day):
    cd = CROPS[crop]
    return {
        "kind": "PLANT",
        "crop": crop,
        "planted_day": day,
        "watered_today": False,
        "consecutive_unwatered": 1,  # planting day counts as unwatered
        "yield_units": 0 if cd["ongoing"] else 1,
        "max_lifespan_step": (-1 if cd["ongoing"] else (day + cd["max_yield_day"] + 1) * turns_per_day),
        "fertilized_until_day": -1,
    }


def _new_plant(crop, day, turns_per_day):
    crop_data = CROPS[crop]
    ongoing = crop_data["ongoing"]
    return {
        "crop": crop,
        "planted_day": day,
        "watered_today": False,
        # Start at 1 so a freshly planted seed dies if it isn't watered on its
        # planting day -- the planting day counts as the first "unwatered" day.
        "consecutive_unwatered": 1,
        # One-time crops start at 1; ongoing crops
        # start at 0 and accumulate via _daily_refresh.
        "yield_units": 0 if ongoing else 1,
        # First step at which decay applies. For one-time crops, decay begins
        # the day AFTER max_yield_day (the peak day). For ongoing crops, set lazily
        # in _daily_refresh once production hits max_yield.
        "max_lifespan_step": (-1 if ongoing else (day + crop_data["max_yield_day"] + 1) * turns_per_day),
    }

