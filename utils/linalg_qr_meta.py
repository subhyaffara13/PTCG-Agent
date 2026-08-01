
def linalg_qr_meta(A: Tensor, mode: str = "reduced") -> tuple[Tensor, Tensor]:
    checkIsMatrix(A, "linalg.qr")
    checkFloatingOrComplex(A, "linalg.qr")

    compute_q, reduced_mode = _parse_qr_mode(mode)

    m = A.shape[-2]
    n = A.shape[-1]
    k = min(m, n)

    if compute_q:
        Q_shape = list(A.shape)
        Q_shape[-1] = k if reduced_mode else m
        Q = A.new_empty(Q_shape)
        Q.as_strided_(Q_shape, make_contiguous_strides_for(Q_shape, row_major=False))
    else:
        Q = A.new_empty([0])

    # For readability
    R_shape = list(A.shape)
    R_shape[-2] = k if reduced_mode or not compute_q else m
    R = A.new_empty(R_shape)
    R.as_strided_(R_shape, make_contiguous_strides_for(R_shape, row_major=False))
    return Q, R

