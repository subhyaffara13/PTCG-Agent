
def conv3d_grid(n, c, d, h, w, meta, *, cdiv):
    return (
        cdiv(n * d * h * w, meta["BLOCK_M"]),
        cdiv(c, meta["BLOCK_N"]),
        meta["GROUPS"],
    )

