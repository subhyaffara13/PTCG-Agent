
def scaled_matmul_wrapper(
    lhs: Array,
    rhs: Array,
    lhs_scales: Array,
    rhs_scales: Array,
    preferred_element_type: DTypeLike = np.dtype('float32'),
) -> Array:
    """
    Performs scaled matrix multiplication between two 3D arrays, with scaling
    factors applied to the matrices.

    Args:
        lhs (Array): A 3D array of shape (B, M, K).
        rhs (Array): A 3D array of shape (B, N, K).
        lhs_scales (Array): A 3D array of shape (B, M, K_block).
        rhs_scales (Array): A 3D array of shape (B, N, K_block).
        preferred_element_type (DTypeLike, optional): The preferred data type
          for the computation. Defaults to `jnp.float32`.

    Returns:
        Array: A 3D array of shape (B, M, N) representing the scaled matrix
          multiplication result.

    Raises:
        AssertionError: If the number of columns in `lhs` (`lhs_K`) does not
          match the number of columns in `rhs` (`rhs_K`).

    Notes:
        - The function ensures that the `preferred_element_type` is
          danonicalized before passing it to the underlying computation.
        - Scaling is applied to the matrices based on the `lhs_scales` and
          `rhs_scales` arrays, enabling efficient computations in blocks.

    """
    B, M, lhs_K = lhs.shape
    _, N, rhs_K = rhs.shape
    assert lhs_K == rhs_K
    _, _, K_block = lhs_scales.shape

    preferred_element_type = dtypes.check_and_canonicalize_user_dtype(
        preferred_element_type, "scaled_matmul_wrapper")

    out = _scaled_matmul(
        lhs,
        rhs,
        lhs_scales,
        rhs_scales,
        preferred_element_type=preferred_element_type,
    )

    return out

