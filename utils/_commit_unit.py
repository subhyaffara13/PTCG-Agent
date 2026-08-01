
def _commit_unit(op, item, price, farm, private, market):
    if op == "SELL":
        if private["shed"].get(item, 0) <= 0:
            return False
        private["shed"][item] -= 1
        farm["money"] += price
        # Sales at $1 do not increase market supply.
        if price > 1:
            market["inventory"][item] += 1
        return True
    if op == "BUY_PRODUCT":
        if farm["money"] < price:
            return False
        farm["money"] -= price
        private["shed"][item] = private["shed"].get(item, 0) + 1
        market["inventory"][item] -= 1
        return True
    if op == "BUY_SEED":
        if farm["money"] < price:
            return False
        farm["money"] -= price
        private["seeds"][item] = private["seeds"].get(item, 0) + 1
        return True
    if op == "BUY_ANIMAL":
        if farm["money"] < price:
            return False
        farm["money"] -= price
        private["shed"][item] = private["shed"].get(item, 0) + 1
        return True
    return False

