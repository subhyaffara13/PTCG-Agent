from typing import Any, Callable

def map_leaves_with_path(
    f: Callable[..., Any | Placeholder],
    *xs: PartsOf[T],
) -> PartsOf[T]:
  """Applies a function to all leaves (present or not), with value path.

  PartsOf-compatible equivalent of `jax_tree_util.tree_map_with_path`.

  Args:
    f: The function to apply to each leaf of the structure. It must accept tree
      path + as many arguments as *xs given here, any number of which may be
      `PLACEHOLDER`. It must return an appropriate non-`None` leaf value, or
      `PLACEHOLDER`.
    *xs: One or more partially known structures.

  Returns:
    A partially known structure.
  """
  x0, *xs = xs
  for x in xs:
    _check_templates_match(x0._template, x._template)  # pylint:disable=protected-access
  def f_(path, _):
    path = tree_utils.tuple_path_from_keypath(path)
    leaves = [x._present.get(path, PLACEHOLDER) for x in (x0, *xs)]  # pylint:disable=protected-access
    result = f(path, *leaves)
    if result is None:
      raise Error(f'At {path}, {f} returned None.')
    if not jax_tree_util.all_leaves([result]):
      raise Error(f'At {path}, {f} returned non-leaf value {result}.')
    return result
  t0 = x0._get_template()  # pylint:disable=protected-access
  return PartsOf(t0, jax_tree_util.tree_map_with_path(f_, t0))

