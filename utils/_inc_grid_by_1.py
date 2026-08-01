
def _inc_grid_by_1(
    indices: tuple[jax.Array, ...], grid: pallas_core.TupleGrid
) -> tuple[jax.Array, ...]:
  next_indices = []
  carry: bool | jax.Array = True
  for idx, size in reversed(list(zip(indices, grid))):
    next_idx = lax.select(carry, idx + 1, idx)
    carry = next_idx == size
    next_indices.append(
        lax.select(carry, jnp.asarray(0, dtype=idx.dtype), next_idx)
    )
  return tuple(reversed(next_indices))

