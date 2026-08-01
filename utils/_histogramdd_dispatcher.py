
def _histogramdd_dispatcher(sample, bins=None, range=None, density=None,
                            weights=None):
    if hasattr(sample, 'shape'):  # same condition as used in histogramdd
        yield sample
    else:
        yield from sample
    with contextlib.suppress(TypeError):
        yield from bins
    yield weights

