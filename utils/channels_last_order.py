
def channels_last_order(rank):
    order = list(reversed(range(rank)))
    order.insert(1, order.pop(-1))
    return order

