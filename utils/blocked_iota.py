
def blocked_iota(block_shape: Shape,
                 total_shape: Shape):
  """Computes a sub-block of a larger shaped iota.

  Args:
    block_shape: The output block shape of the iota.
    total_shape: The total shape of the input tensor.
  Returns:
    Result of the blocked iota.
  """
  iota_data = jnp.zeros(block_shape, dtype=jnp.uint32)
  multiplier = 1
  for dim in range(len(block_shape)-1, -1, -1):
    block_mult = 1
    counts_lo = lax.broadcasted_iota(
        dtype=jnp.uint32, shape=block_shape, dimension=dim
    )
    iota_data += counts_lo * multiplier * block_mult
    multiplier *= total_shape[dim]
  return iota_data

