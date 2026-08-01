
def scaled_matmul(
    lhs: Array,
    rhs: Array,
    lhs_scales: Array,
    rhs_scales: Array,
    preferred_element_type: DTypeLike = np.float32,
) -> Array:
    r"""Scaled matrix multiplication function.

    Performs block-scaled matmul of `a` and `b` using `a_scales` and `b_scales`.
    The last dim is the contracting dim, and block size is inferred.

    Mathematically, this operation is equivalent to::

      a_block_size = a.shape[-1] // a_scales.shape[-1]
      b_block_size = b.shape[-1] // b_scales.shape[-1]
      a_scaled = a * jnp.repeat(a_scales, a_block_size, axis=-1)
      b_scaled = b * jnp.repeat(b_scales, b_block_size, axis=-1)
      jnp.einsum('BMK,BNK->BMN', a_scaled, b_scaled)

    Args:
      lhs (Array): Operand a, shape (B, M, K).
      rhs (Array): Operand b, shape (B, N, K).
      lhs_scales (Array): Shape (B, M, K_a), where `K % K_a == 0`.
      rhs_scales (Array): Shape (B, N, K_b), where `K % K_b == 0`.
      preferred_element_type (DTypeLike, optional): Defaults to `jnp.float32`.

    Returns:
      Array of shape (B, M, N).

    Notes:
      - We currently do not support user-defined `precision` for customizing the
        compute data type. It is fixed to `jnp.float32`.
      - Block size is inferred as `K // K_a` for `a` and `K // K_b` for `b`.
      - To use cuDNN with Nvidia Blackwell GPUs, inputs must match::

          # mxfp8
          a, b: jnp.float8_e4m3fn | jnp.float8_e5m2
          a_scales, b_scales: jnp.float8_e8m0fnu
          block_size: 32
          # nvfp4
          a, b: jnp.float4_e2m1fn
          a_scales, b_scales: jnp.float8_e4m3fn
          block_size: 16

    Examples:

      Basic case:

      >>> a = jnp.array([1, 2, 3]).reshape((1, 1, 3))
      >>> b = jnp.array([4, 5, 6]).reshape((1, 1, 3))
      >>> a_scales = jnp.array([0.5]).reshape((1, 1, 1))
      >>> b_scales = jnp.array([0.5]).reshape((1, 1, 1))
      >>> scaled_matmul(a, b, a_scales, b_scales)  # doctest: +SKIP
      Array([[[8.]]], dtype=float32)

      Using fused cuDNN call on Blackwell GPUs:

      >>> dtype = jnp.float8_e4m3fn
      >>> a = jax.random.normal(jax.random.PRNGKey(1), (3, 128, 64), dtype=dtype)
      >>> b = jax.random.normal(jax.random.PRNGKey(2), (3, 128, 64), dtype=dtype)
      >>> a_scales = jnp.ones((3, 128, 4), dtype=jnp.float8_e8m0fnu)
      >>> b_scales = jnp.ones((3, 128, 4), dtype=jnp.float8_e8m0fnu)
      >>> scaled_matmul(a, b, a_scales, b_scales)  # doctest: +SKIP
    """
    a, b, a_scales, b_scales = lhs, rhs, lhs_scales, rhs_scales
    if not all(x.ndim == 3 for x in (a, b, a_scales, b_scales)):
        raise ValueError(
            "scaled_matmul requires all inputs to be 3-dimensional arrays"
        )

    B_a, M_a, K_a = a.shape
    B_b, N_b, K_b = b.shape
    if K_a != K_b or B_a != B_b:
        raise ValueError(
            "scaled_matmul requires inputs a and b to have matching batch (B) "
            f"and contract (K) dimensions, but got shapes {a.shape} and "
            f"{b.shape}"
        )

    B_as, M_as, K_as = a_scales.shape
    B_bs, N_bs, K_bs = b_scales.shape
    if K_as != K_bs or B_as != B_bs:
        raise ValueError(
            "scaled_matmul requires scales to have matching batch (B) and "
            f"contract (K) dimensions, but got shapes {a_scales.shape} and "
            f"{b_scales.shape}"
        )

    if M_as != M_a or N_bs != N_b:
        raise ValueError(
            "scaled_matmul requires scales to match non-contract dimensions of "
            f"inputs, but got shapes a: {a.shape}, b: {b.shape}, a_scales: "
            f"{a_scales.shape}, b_scales: {b_scales.shape}"
        )

    preferred_element_type = dtypes.check_and_canonicalize_user_dtype(
        preferred_element_type, "scaled_matmul"
    )
    out = cudnn_scaled_matmul(
        a,
        b,
        a_scales,
        b_scales,
        preferred_element_type=preferred_element_type,
    )
    return out

