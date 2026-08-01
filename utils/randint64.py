
def randint64(seed, offset, low, high):
    r0, r1, _r2, _r3 = randint4x(seed, offset, PHILOX_N_ROUNDS_DEFAULT)
    r0 = hl.cast(hl.UInt(64), r0)
    r1 = hl.cast(hl.UInt(64), r1)

    result = r0 | (r1 << 32)
    size = high - low
    result = result % hl.cast(hl.UInt(64), size)
    result = hl.cast(hl.Int(64), result) + low
    return result


def randint64(seed, offset, low, high):
    r0, r1, _r2, _r3 = tl.randint4x(seed, offset)
    r0 = r0.to(tl.uint64)
    r1 = r1.to(tl.uint64)
    result = r0 | (r1 << 32)
    size = high - low
    result = result % size.to(tl.uint64)
    result = result.to(tl.int64) + low
    return result

