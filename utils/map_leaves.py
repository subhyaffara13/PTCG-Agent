from typing import Any, Callable

def map_leaves(
    f: Callable[..., Any | Placeholder],
    *xs: PartsOf[T],
) -> PartsOf[T]:
  """Applies a function to all leaves (present or not).

  PartsOf-compatible equivalent of `jax.tree.map`.

  Args:
    f: The function to apply to each leaf of the structure. It must accept as
        many arguments as given here, any number of which may be `PLACEHOLDER`.
        It must return an appropriate non-`None` leaf value, or `PLACEHOLDER`.
    *xs: One or more partially known structures.

  Returns:
    A partially known structure.
  """
  def _wrapped_f(path, *leaves):
    del path
    return f(*leaves)

  return map_leaves_with_path(_wrapped_f, *xs)

