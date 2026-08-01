
def _refresh_prices(market):
    params = market.get("params")
    for item in PRODUCTS:
        market["prices"][item] = market_price(item, market["inventory"][item], params)

