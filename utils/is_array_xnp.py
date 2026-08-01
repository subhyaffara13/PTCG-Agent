
def is_array_xnp(x, xnp) -> bool:
  """`isinstance(x, xnp.Array)`."""
  if lazy.has_torch and xnp is lazy.torch:
    return isinstance(x, xnp.Tensor)
  else:
    return isinstance(x, xnp.ndarray)

