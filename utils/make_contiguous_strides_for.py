
def make_contiguous_strides_for(
    shape: ShapeType, row_major: bool = True
) -> tuple[_IntLikeT | int, ...]:
    """
    Returns the strides of a contiguous tensor if row_major
    If row_major=True, it returns the strides of a contiguous batch of Fortran-contiguous matrices
    This is often used when calling external libraries like BLAS/LAPACK/cuSolver...
    """
    # contiguous_strides from c10/util/strides.h
    validate_shape(shape)
    if not shape:
        return ()

    from torch.fx.experimental.symbolic_shapes import is_nested_int

    multiplier: _IntLikeT | int = 1
    strides = []
    for l in reversed(shape):
        strides.append(multiplier)
        multiplier *= l if is_nested_int(l) else sym_max(l, 1)  # type:ignore[assignment]

    result = tuple(reversed(strides))

    # batched_matrix_contiguous_strides from aten/src/ATen/native/LinearAlgebraUtils.h
    if row_major:
        return result
    else:
        if len(shape) < 2:
            return result
        # Use sym_max to handle unbacked symbolic dimensions
        return result[:-2] + (1, sym_max(shape[-2], 1))

