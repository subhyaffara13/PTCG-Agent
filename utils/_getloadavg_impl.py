
def _getloadavg_impl():
    # Drop to 2 decimal points which is what Linux does
    raw_loads = cext.getloadavg()
    return tuple(round(load, 2) for load in raw_loads)

