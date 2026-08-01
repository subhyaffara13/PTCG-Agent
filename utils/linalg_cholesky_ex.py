
def linalg_cholesky_ex(A: Tensor, upper: bool = False, check_errors: bool = False):
    squareCheckInputs(A, "linalg.cholesky")
    checkFloatingOrComplex(A, "linalg.cholesky")

    A_shape = A.shape
    ndim = len(A_shape)

    # L
    L_strides = make_contiguous_strides_for(A_shape, False)
    L = A.new_empty(A_shape)
    L.as_strided_(A_shape, L_strides)

    # infos
    infos = A.new_empty(A_shape[0 : ndim - 2], dtype=torch.int32)
    return L, infos

