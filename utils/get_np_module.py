
def get_np_module(array: Array, *, strict: bool = True):  # -> NpModule:
  """Returns the numpy module associated with the given array.

  Args:
    array: Either tf, jax or numpy array.
    strict: If `False`, default to `np.array` if the array can't be infered (
      to support array-like: list, tuple,...)

  Returns:
    The numpy module.
  """
  return lazy.get_xnp(array, strict=strict)

