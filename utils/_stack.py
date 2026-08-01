
def _stack(arrs: Sequence[Array], axis: int=0) -> Array:
  return lax.concatenate([lax.expand_dims(arr, (axis,)) for arr in arrs], dimension=axis)


def _stack(*arrs: Array) -> Array:
  """Stack arrays together."""
  xnp = enp.lazy.get_xnp(arrs[0])
  return xnp.stack(arrs)

