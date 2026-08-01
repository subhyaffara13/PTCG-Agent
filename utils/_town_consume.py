
def _town_consume(env, state, step):
    obs0 = state[0].observation
    market = obs0.market
    town = obs0.town
    cfg = env.configuration
    shop_interval = max(1, int(get(cfg, "townShopSellInterval", 4)))
    center_interval = max(1, int(get(cfg, "townCenterSellInterval", 12)))
    turns_per_day = max(1, int(get(cfg, "turnsPerDay", 24)))
    day = step // turns_per_day

    if step % shop_interval == 0:
        for shop_name in town.get("unlocked_shops", []):
            products = SHOPS[shop_name]
            multiplier = 2 if len(products) == 1 else 1
            for item in products:
                market["inventory"][item] -= multiplier

    if step % center_interval == 0:
        center_mult = next(m for threshold, m in TOWN_CENTER_DEMAND_SCHEDULE if day >= threshold)
        for item in TOWN_CENTER_PRODUCTS:
            market["inventory"][item] -= center_mult

    _refresh_prices(market)

