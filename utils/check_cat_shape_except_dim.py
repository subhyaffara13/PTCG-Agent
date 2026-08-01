
def check_cat_shape_except_dim(
    first: list[int], second: list[int], dimension: int, index: int
):
    first_dims = len(first)
    second_dims = len(second)
    if first_dims != second_dims:
        raise AssertionError(
            f"Tensors must have same number of dimensions, got {first_dims} and "
            f"{second_dims}"
        )
    for dim in range(0, first_dims):
        if dim != dimension:
            if first[dim] != second[dim]:
                raise AssertionError(
                    f"Sizes of tensors must match except in dimension {dimension}, "
                    f"got {first[dim]} and {second[dim]} at dimension {dim}"
                )

