
def meta__linalg_eigh(A: Tensor, UPLO: str = "L", compute_v: bool = True):
    squareCheckInputs(A, "linalg.eigh")
    checkUplo(UPLO)

    shape = list(A.shape)
    if compute_v:
        vecs = A.new_empty(shape)
        vecs.as_strided_(shape, make_contiguous_strides_for(shape, row_major=False))
    else:
        vecs = A.new_empty([0])

    shape.pop()
    vals = A.new_empty(shape, dtype=toRealValueType(A.dtype))

    return vals, vecs

