
def _prev_index(
    indices: tuple[int | jax.Array, ...], grid: tuple[int | jax.Array, ...]
) -> tuple[int | jax.Array, ...]:
  out = []
  borrow: bool | jax.Array = True
  for i, g in reversed(list(zip(indices, grid, strict=True))):
    dec = jax.lax.select(borrow, i - 1, i)
    borrow = dec == -1
    out.append(jax.lax.select(borrow, g - 1, dec))
  return _filter_indices(tuple(reversed(out)), grid)

