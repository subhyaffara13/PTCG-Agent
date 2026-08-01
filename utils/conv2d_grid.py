
def conv2d_grid(n, c, h, w, meta, *, cdiv):
    return (
        cdiv(n * h * w, meta["BLOCK_M"]),
        cdiv(c, meta["BLOCK_N"]),
        meta["GROUPS"],
    )

