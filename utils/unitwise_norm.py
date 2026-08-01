
def unitwise_norm(
    x: jax.typing.ArrayLike, axis: Optional[Union[int, tuple[int, ...]]] = None
) -> jax.Array:
  """Computes the L2 norm of each unit separately.

  A "unit" is a slice of `x` along the dimensions specified by `axis`. If `axis`
  is ``None``, the reduction axes are inferred from `x`'s rank based on
  common layer conventions:
    - Rank-1: The whole vector.
    - Rank-2: Axis 0 (e.g., for linear layers).
    - Rank-3 or 4: Axes (0, 1, 2) (e.g., for multi-head attention or
      convolutions).
    - Rank-5: Axes (0, 1, 2, 3) (e.g., for Conv3D kernels with spatial dims).

  Args:
    x: Input array for which to compute unit-wise norms.
    axis: Axis or axes to normalize over. If ``None``, defaults are
      inferred from the input's rank.

  Returns:
    Array with the same shape as `x`, where each unit is replaced by its
    L2 norm.
  """
  if axis is not None:
    # Use provided axes for reduction
    squared_norm = jnp.sum(numerics.abs_sq(x), axis=axis, keepdims=True)
  elif jnp.squeeze(x).ndim <= 1:  # Scalars and vectors
    squared_norm = jnp.sum(numerics.abs_sq(x), keepdims=True)
  # Note that this assumes parameters with a shape of length 3 are multihead
  # linear parameters--if you wish to apply AGC to 1D convs, you may need
  # to modify this line.
  elif x.ndim in (2, 3):  # Linear layers of shape IO or multihead linear  # pytype: disable=attribute-error  # jax-arraylike # noqa: E501
    squared_norm = jnp.sum(numerics.abs_sq(x), axis=0, keepdims=True)
  elif x.ndim == 4:  # Conv kernels of shape HWIO  # pytype: disable=attribute-error  # jax-arraylike # noqa: E501
    squared_norm = jnp.sum(numerics.abs_sq(x), axis=(0, 1, 2), keepdims=True)
  elif x.ndim == 5:  # Conv3D kernels of shape DHWIO  # pytype: disable=attribute-error  # jax-arraylike # noqa: E501
    squared_norm = jnp.sum(numerics.abs_sq(x), axis=(0, 1, 2, 3), keepdims=True)
  else:
    raise ValueError(
        f"Expected parameter with shape in {1, 2, 3, 4, 5}, got {x.shape}. "  # pytype: disable=attribute-error  # jax-arraylike # noqa: E501
        "Use axis parameter to specify reduction axes for other shapes."
    )
  return jnp.broadcast_to(jnp.sqrt(squared_norm), x.shape)  # pytype: disable=attribute-error  # jax-arraylike # noqa: E501

