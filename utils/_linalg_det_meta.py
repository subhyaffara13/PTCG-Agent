
def _linalg_det_meta(A):
    squareCheckInputs(A, "linalg.det")
    checkFloatingOrComplex(A, "linalg.det")

    det = A.new_empty(A.shape[:-2])

    LU = A.new_empty(A.shape)
    LU.as_strided_(A.shape, make_contiguous_strides_for(A.shape, row_major=False))

    pivots = A.new_empty(A.shape[:-1], dtype=torch.int32)
    return det, LU, pivots

