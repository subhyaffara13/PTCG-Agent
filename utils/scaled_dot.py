
def scaled_dot(
    lhs: Array,
    rhs: Array,
    *,
    lhs_scale: Array | None = None,
    rhs_scale: Array | None = None,
    dimension_numbers: lax.DotDimensionNumbers | None = None,
    preferred_element_type: DTypeLike | None = None,
):
  """Computes a scaled dot product.

  This function computes `(lhs * lhs_scale) @ (rhs * rhs_scale)` in
  `preferred_element_type` precision, where `@` denotes `jax.lax.dot_general`.

  Non-contracting dimensions of the operand and scale must have the same size.
  Contracting dimension size of the operand must be an integer multiple of the
  scale contracting dimension size (subchannel size). Latency of the op depends
  on what subchannel sizes are natively supported on your platform.

  .. note::
    This currently isn't differentiable (no transpose rule).

  Example:
    ::

      B = 32
      M = 16384
      N = 16
      K = 4096
      subchannel_size = 32

      lhs_shape = (B, M, K)
      rhs_shape = (B, K, N)
      lhs_scales_shape = (B, M, K // subchannel_size)
      rhs_scales_shape = (B, K // subchannel_size, N)

      key = jax.random.key(42)

      lhs = jax.random.normal(key, lhs_shape, dtype=jnp.float8_e4m3fn)
      rhs = jax.random.normal(key, rhs_shape, dtype=jnp.float8_e4m3fn)
      lhs_scales = jax.random.normal(
          key, lhs_scales_shape, dtype=jnp.float8_e8m0fnu
      )
      rhs_scales = jax.random.normal(
          key, rhs_scales_shape, dtype=jnp.float8_e8m0fnu
      )

      @jax.jit
      def scaled_dot_fn(lhs, rhs, lhs_scale, rhs_scale):
        return jax.lax.scaled_dot(
            lhs,
            rhs,
            lhs_scale=lhs_scale,
            rhs_scale=rhs_scale,
            preferred_element_type=jnp.bfloat16,
        )

      result = scaled_dot_fn(
          lhs,
          rhs,
          lhs_scale=lhs_scales,
          rhs_scale=rhs_scales,
      )

  Args:
    lhs: The left-hand side operand of the dot product.
    rhs: The right-hand side operand of the dot product.
    lhs_scale: The scale factor for `lhs`. It should be at least 2x smaller
      along the contracting dimension as compared to the operand.
    rhs_scale: The scale factor for `rhs`. It should be at least 2x smaller
      along the contracting dimension as compared to the operand.
    dimension_numbers: A tuple of tuples of the form `((lhs_contracting_dims,
      rhs_contracting_dims), (lhs_batch_dims, rhs_batch_dims))`. If not
      provided, default is `(((1,), (0,)), ((), ()))` for 2D inputs which is
      lhs_contracting_dim=1, rhs_contracting_dim=0, and `(((2,), (1,)), ((0,),
      (0,)))` for 3D inputs which is lhs_contracting_dim=2,
      rhs_contracting_dim=1 and lhs_batch_dim=0, rhs_batch_dim=0.
    preferred_element_type: The desired dtype of the output and intermediate
      accumulations, can be `bfloat16` or `float32`. Defaults to `bfloat16`.

  Returns:
    The result of the scaled dot product.
  """

  # Syntax sugar for dimension numbers it allows for None to be passed for the
  # default case.
  if dimension_numbers is None:
    if lhs.ndim == 0 or lhs.ndim == 1:
      raise TypeError("scaled_dot does not support 0-rank and 1-rank operands.")
    else:
      n = lhs.ndim
      dimension_numbers = (
          ((n - 1,), (n - 2,)),
          (tuple(range(n - 2)), tuple(range(n - 2))),
      )

  (lhs_contracting, rhs_contracting), _ = dimension_numbers

  if lhs_scale is None:
    lhs_scale = _create_dummy_scale(lhs, lhs_contracting)

  if rhs_scale is None:
    rhs_scale = _create_dummy_scale(rhs, rhs_contracting)

  element_type = (
      preferred_element_type
      if preferred_element_type is not None
      else dtypes.bfloat16
  )
  element_type = dtypes.check_and_canonicalize_user_dtype(
      element_type, "scaled_dot"
  )
  return scaled_dot_p.bind(
      lhs,
      rhs,
      lhs_scale,
      rhs_scale,
      dimension_numbers=dimension_numbers,
      preferred_element_type=element_type,
  )

