
def _do_hire(farm, private, board_size, mult=FARM_HAND_COST_MULT):
    cost = _hire_cost(farm["hires_today"], mult)
    if farm["money"] < cost:
        return
    farm["money"] -= cost
    farm["hires_today"] += 1
    farm["hands"].append(_spawn_hand(farm, board_size))
    private["inventories"].append({})

