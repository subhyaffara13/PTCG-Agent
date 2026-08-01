
def b2b_gemm_grid(M, P, meta, *, cdiv):
    return (cdiv(M, meta["BLOCK_SIZE_M"]) * cdiv(P, meta["BLOCK_SIZE_P"]), 1, 1)

