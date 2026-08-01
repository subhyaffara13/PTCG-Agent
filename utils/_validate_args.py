
def _validate_args(
    *,
    lhs: jnp.ndarray,
    rhs: jnp.ndarray,
    group_sizes: jnp.ndarray,
    expected_rhs_dims: int = 3,
) -> tuple[jnp.ndarray, jnp.ndarray, jnp.dtype]:
  """Validates the arguments for the gmm function."""
  # Validate 'lhs'.
  if lhs.ndim != 2:
    raise ValueError(f"Expected 2-tensor for 'lhs' but got {lhs.ndim}-tensor.")
  common.assert_is_supported_dtype(lhs.dtype)

  # Validate 'rhs'.
  if rhs.ndim != expected_rhs_dims:
    raise ValueError(
        f"Expected {expected_rhs_dims}-tensor for 'rhs' but got"
        f" {rhs.ndim}-tensor."
    )
  common.assert_is_supported_dtype(rhs.dtype)

  # Validate 'group_sizes'.
  if group_sizes.dtype != jnp.int32:
    raise ValueError(
        f"Expected 32-bit integer 'group_sizes' but got {group_sizes.dtype}."
    )

  return lhs, group_sizes, common.select_input_dtype(lhs, rhs)

