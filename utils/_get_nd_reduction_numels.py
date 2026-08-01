
def _get_nd_reduction_numels(r: int, size_hints: dict[str, int]) -> dict[str, int]:
    """
    Converts a linear reduction numel to ND, in row major order.
    This order is often desirable as it presents opportunities to coalesce memory
    accesses.
    For example, if r = 64 and size_hints = [32,32], this function returns [32, 2].
    This unraveling works because both r and size_hints are powers of 2.
    """
    # Shrink r to size_hints.
    r = min(r, get_total_reduction_numel(size_hints))
    num_reduction_dims = len(
        [prefix for prefix in size_hints if prefix_is_reduction(prefix)]
    )

    remaining = r
    rnumels = {}
    for idx in range(num_reduction_dims - 1, -1, -1):
        prefix = f"r{idx}_"
        max_size = min(size_hints[prefix], TRITON_MAX_BLOCK[prefix.upper()])
        dim = min(max_size, remaining)
        assert remaining % dim == 0, (
            f"Expected dimension '{dim}' to divide remaining size '{remaining}'"
        )
        rnumels[prefix] = dim
        remaining //= dim

    # Sanity check the results.
    final_numel = conditional_product(*rnumels.values())
    assert r == final_numel, (
        f"Expected ND reduction size ({rnumels}) to have {r} elements."
    )
    assert all(rnumels[prefix] <= size_hints[prefix] for prefix in rnumels), (
        f"rnumels exceed size_hints. {rnumels} > {size_hints}"
    )

    return rnumels

