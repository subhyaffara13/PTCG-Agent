
def is_literalable(x: Any, for_ad: bool = False) -> bool:
  x_type = type(x)
  # Faster path for scalar types, which avoids an np.ndarray conversion.
  if x_type in literalable_scalar_types:
    return True

  # See https://docs.jax.dev/en/latest/internals/constants.html
  # for_ad: we want to preserve under AD
  if config.use_simplified_jaxpr_constants.value:
    from jax._src.array import ArrayImpl  # pyrefly: ignore[missing-import]
    do_lit_array = not for_ad
    if isinstance(x, ArrayImpl):
      return do_lit_array
  else:
    do_lit_array = False
  for t in x_type.__mro__:
    if t in literalable_types:
      return (do_lit_array or not np.ndim(x))
  return False

