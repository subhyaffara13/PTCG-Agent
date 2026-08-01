
def halide_philox(seed, c0, c1, c2, c3, n_rounds):
    seed = hl.cast(hl.UInt(64), seed)

    assert c0.type().bits() == 32

    seed_hi = hl.cast(hl.UInt(32), (seed >> 32) & hl.u64(0xFFFFFFFF))
    seed_lo = hl.cast(hl.UInt(32), seed & hl.u64(0xFFFFFFFF))

    return philox_impl(c0, c1, c2, c3, seed_lo, seed_hi, n_rounds)

