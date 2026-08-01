
def _next_index(
    indices: tuple[int | jax.Array, ...], grid: tuple[int | jax.Array, ...],
    allow_overflow: bool = False,
) -> tuple[int | jax.Array, ...]:
  """Increments the grid indices by one.

  Args:
    indices: the current grid indices.
    grid: the pallas grid.
    allow_overflow: whether to allow the indices to overflow the grid.
      If False (default), indices will wrap around to zero after reaching the
      maximum grid size. If True, the bounds on the first grid position
      will be ignored.

  Returns:
    The next grid indices.
  """
  out = []
  carry: bool | jax.Array = True
  for position, (i, g) in enumerate(
      reversed(list(zip(indices, grid, strict=True)))):
    inc = jax.lax.select(carry, i + 1, i)
    if allow_overflow and (position == len(grid) - 1):
      carry = False
    else:
      carry = inc == g
    out.append(jax.lax.select(carry, 0, inc))
  if allow_overflow:
    return tuple(reversed(out))
  else:
    return _filter_indices(tuple(reversed(out)), grid)

