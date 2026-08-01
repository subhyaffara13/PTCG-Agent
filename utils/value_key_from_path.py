
def value_key_from_path(path: tuple[Any, ...]) -> tuple[Any, ...]:
  """Converts a PartsOf JAX pytree path into a key for the corresponding value.

  Args:
    path: a JAX tree path into a PartsOf object (i.e. obtained via one of
      `jax_tree_util.*` methods on a PartsOf pytree).

  Returns:
    A key for the corresponding value in PartsOf template's flattened dict
    (i.e. `_present`).
  """
  assert len(path) == 2, (
      f'Too many elements in a PartsOf tree path: {path}, expected 2.'
  )
  assert isinstance(
      path[1], jax_tree_util.DictKey
  ), f'Expected DictKey, found: {path[1]}'
  return path[1].key

