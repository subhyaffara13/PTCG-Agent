
def rand_eager_kernel(seed, offset_blocks, tid, VEC, n_rounds=PHILOX_N_ROUNDS_DEFAULT):
    inv = hl.cast(hl.Float(32), 1.0 / 4294967296.0)  # 2^-32
    half = hl.cast(hl.Float(32), 0.5) * inv

    tid_u64 = hl.cast(hl.UInt(64), tid)
    VEC_u64 = hl.cast(hl.UInt(64), VEC)
    subseq = tid_u64 // VEC_u64
    which4 = (tid_u64 % VEC_u64) // hl.cast(hl.UInt(64), 4)
    lane = tid_u64 % hl.cast(hl.UInt(64), 4)

    offblk = hl.cast(hl.UInt(64), offset_blocks) + which4

    c0 = hl.cast(hl.UInt(32), offblk & hl.cast(hl.UInt(64), 0xFFFFFFFF))
    c1 = hl.cast(
        hl.UInt(32),
        (offblk >> hl.cast(hl.UInt(64), 32)) & hl.cast(hl.UInt(64), 0xFFFFFFFF),
    )
    c2 = hl.cast(hl.UInt(32), subseq & hl.cast(hl.UInt(64), 0xFFFFFFFF))
    c3 = hl.cast(
        hl.UInt(32),
        (subseq >> hl.cast(hl.UInt(64), 32)) & hl.cast(hl.UInt(64), 0xFFFFFFFF),
    )

    u0, u1, u2, u3 = halide_philox(seed, c0, c1, c2, c3, n_rounds)

    v01 = hl.select(lane == hl.cast(hl.UInt(64), 0), u0, u1)
    v23 = hl.select(lane == hl.cast(hl.UInt(64), 2), u2, u3)
    rand_int = hl.select(
        (lane == hl.cast(hl.UInt(64), 0)) | (lane == hl.cast(hl.UInt(64), 1)), v01, v23
    )

    return hl.cast(hl.Float(32), 1.0) - (hl.cast(hl.Float(32), rand_int) * inv + half)


def rand_eager_kernel(seed, offset_blocks, tid: tl.tensor, VEC: tl.constexpr):
    inv = 1.0 / 4294967296.0
    half = inv * 0.5

    tid_u64 = tid.to(tl.uint64)

    subseq = tid_u64 // VEC
    which4 = (tid_u64 % VEC) // 4
    lane = tid_u64 % 4

    offblk = offset_blocks.to(tl.uint64) + which4

    u0, u1, u2, u3 = tl.philox(
        seed,
        (offblk & 0xFFFFFFFF).to(tl.uint32),
        ((offblk >> 32) & 0xFFFFFFFF).to(tl.uint32),
        (subseq & 0xFFFFFFFF).to(tl.uint32),
        ((subseq >> 32) & 0xFFFFFFFF).to(tl.uint32),
    )

    v01 = tl.where(lane == 0, u0, u1)
    v23 = tl.where(lane == 2, u2, u3)
    rand_int = tl.where((lane == 0) | (lane == 1), v01, v23)

    return 1.0 - (rand_int.to(tl.float32) * inv + half)

