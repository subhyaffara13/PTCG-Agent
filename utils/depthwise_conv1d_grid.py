
def depthwise_conv1d_grid(n, c, l, meta, *, cdiv):
    return (
        cdiv(n, meta["BLOCK_N"]),
        cdiv(l, meta["BLOCK_L"]),
        cdiv(c, meta["BLOCK_C"]),
    )

