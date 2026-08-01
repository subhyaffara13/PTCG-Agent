
def _uint_to_uniform_float(x):
    """
    Numerically stable function to convert a random uint into a random float uniformly sampled in [0, 1).
    """

    # TODO:
    # conditions can be simplified
    # scale is ((2**23 - 1) / 2**23) * 2**(N_BITS - 1)
    # https://github.com/triton-lang/triton/blob/e4a0d93ff1a367c7d4eeebbcd7079ed267e6b06f/python/triton/language/random.py#L116-L132.
    assert x.type() == hl.UInt(32) or x.type() == hl.Int(32)
    x = hl.cast(hl.Int(32), x)
    scale = hl.f64(4.6566127342e-10)
    x = hl.select(x < 0, -x - 1, x)
    return x * scale

