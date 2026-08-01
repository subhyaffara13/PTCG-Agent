
def _item(self: Array, *args: int) -> bool | int | float | complex:
  """Copy an element of an array to a standard Python scalar and return it."""
  arr = core.concrete_or_error(np.asarray, self, context="This occurred in the item() method of jax.Array")
  if dtypes.issubdtype(self.dtype, dtypes.extended):
    raise TypeError(f"No Python scalar type for {arr.dtype=}")
  return arr.item(*args)

