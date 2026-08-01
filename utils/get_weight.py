
def get_weight(m):
    result = getattr(m, 'weight', None)
    if result is not None:
        return result
    return getattr(m, 'weights', None)

