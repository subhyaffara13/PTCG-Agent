
def default_index(n: int) -> RangeIndex:
    rng = range(n)
    return RangeIndex._simple_new(rng, name=None)

