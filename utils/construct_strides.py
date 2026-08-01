
def construct_strides(
    sizes: Sequence[_IntLike],
    fill_order: Sequence[int],
) -> Sequence[_IntLike]:
    """From a list of sizes and a fill order, construct the strides of the permuted tensor."""
    # Initialize strides
    assert len(sizes) == len(fill_order), (
        "Length of sizes must match the length of the fill order"
    )
    strides: list[_IntLike] = [0] * len(sizes)

    # Start with stride 1 for the innermost dimension
    current_stride: _IntLike = 1

    # Iterate through the fill order populating strides
    for dim in fill_order:
        strides[dim] = current_stride
        current_stride *= sizes[dim]

    return strides

