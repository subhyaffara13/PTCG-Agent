
def _indices_to_layout(indices: list[int]) -> tuple[tuple[int, ...], tuple[int, ...]]:
    # Base case: A single index represents a point, not a dimension.
    if len(indices) <= 1:
        return (), ()

    # The smallest stride is likely the GCD of the differences between consecutive indices.
    # For a sorted, unique list, all differences will be positive.
    diffs = [indices[i] - indices[i - 1] for i in range(1, len(indices))]
    last_stride = _gcd_list(diffs)

    # This case should not be reached if indices are unique and sorted.
    if last_stride == 0:
        raise AssertionError("Cannot determine stride; indices may not be unique.")

    # Identify the starting index of each "row" in the last dimension.
    # An index starts a new row if the preceding index (index - stride) is not present.
    indices_set = set(indices)
    higher_dim_indices = [indices[0]]
    for index in indices[1:]:
        if (index - last_stride) not in indices_set:
            higher_dim_indices.append(index)

    # From the number of rows, we can deduce the shape of the last dimension.
    if len(indices) % len(higher_dim_indices) != 0:
        raise AssertionError(
            "Indices do not form a regular grid. "
            f"Found {len(higher_dim_indices)} subgroups for {len(indices)} total elements."
        )
    last_shape = len(indices) // len(higher_dim_indices)

    # Recurse on the higher-dimensional indices (the start of each row).
    higher_shapes, higher_strides = _indices_to_layout(higher_dim_indices)

    # Combine the results from the recursion with the current dimension's results.
    final_shapes = higher_shapes + (last_shape,)
    final_strides = higher_strides + (last_stride,)

    return final_shapes, final_strides

