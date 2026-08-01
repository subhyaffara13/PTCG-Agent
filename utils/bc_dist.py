
def bc_dist(expr):
    """ Turn  a*[X, Y] into [a*X, a*Y] """
    factor, mat = expr.as_coeff_mmul()
    if factor == 1:
        return expr

    unpacked = unpack(mat)

    if isinstance(unpacked, BlockDiagMatrix):
        B = unpacked.diag
        new_B = [factor * mat for mat in B]
        return BlockDiagMatrix(*new_B)
    elif isinstance(unpacked, BlockMatrix):
        B = unpacked.blocks
        new_B = [
            [factor * B[i, j] for j in range(B.cols)] for i in range(B.rows)]
        return BlockMatrix(new_B)
    return expr

