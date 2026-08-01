
def _histogram2d_dispatcher(x, y, bins=None, range=None, density=None,
                            weights=None):
    yield x
    yield y

    # This terrible logic is adapted from the checks in histogram2d
    try:
        N = len(bins)
    except TypeError:
        N = 1
    if N == 2:
        yield from bins  # bins=[x, y]
    else:
        yield bins

    yield weights

