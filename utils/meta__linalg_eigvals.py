
def meta__linalg_eigvals(input: Tensor) -> Tensor:
    squareCheckInputs(input, "linalg.eigvals")
    complex_dtype = (
        input.dtype
        if utils.is_complex_dtype(input.dtype)
        else utils.corresponding_complex_dtype(input.dtype)
    )
    return input.new_empty(input.shape[:-1], dtype=complex_dtype)

