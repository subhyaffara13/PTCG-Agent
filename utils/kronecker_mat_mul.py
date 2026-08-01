
def kronecker_mat_mul(expr):
    # modified from block matrix code
    factor, matrices = expr.as_coeff_matrices()

    i = 0
    while i < len(matrices) - 1:
        A, B = matrices[i:i+2]
        if isinstance(A, KroneckerProduct) and isinstance(B, KroneckerProduct):
            matrices[i] = A._kronecker_mul(B)
            matrices.pop(i+1)
        else:
            i += 1

    return factor*MatMul(*matrices)

