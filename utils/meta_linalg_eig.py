
def meta_linalg_eig(input: Tensor):
    squareCheckInputs(input, "linalg.eig")
    complex_dtype = (
        input.dtype
        if utils.is_complex_dtype(input.dtype)
        else utils.corresponding_complex_dtype(input.dtype)
    )
    values = input.new_empty(input.shape[:-1], dtype=complex_dtype)
    vectors = input.new_empty(input.shape, dtype=complex_dtype)
    is_cuda = device_hint(input) == "cuda"
    vectors.as_strided_(
        input.shape, make_contiguous_strides_for(input.shape, row_major=is_cuda)
    )
    return values, vectors

