
def randint4x(seed, offset, n_rounds):
    offset = hl.cast(hl.UInt(32), offset)
    _0 = hl.u32(0)
    return halide_philox(seed, offset, _0, _0, _0, n_rounds)

