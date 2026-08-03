from typing import Any, Callable

def path_aware_map(
  f: Callable[[PathParts, Any], Any], nested_dict: VariableDict
) -> VariableDict:
  """A map function that operates over nested dictionary structures while taking
  the path to each leaf into account.

  Example::

    >>> import jax.numpy as jnp
    >>> from flax import traverse_util

    >>> params = {'a': {'x': 10, 'y': 3}, 'b': {'x': 20}}
    >>> f = lambda path, x: x + 5 if 'x' in path else -x
    >>> traverse_util.path_aware_map(f, params)
    {'a': {'x': 15, 'y': -3}, 'b': {'x': 25}}

  Args:
    f: A callable that takes in ``(path, value)`` arguments and maps them
      to a new value. Here ``path`` is a tuple of strings.
    nested_dict: A nested dictionary structure.

  Returns:
    A new nested dictionary structure with the mapped values.
  """
  flat = flatten_dict(nested_dict, keep_empty_nodes=True)
  return unflatten_dict(
    {k: f(k, v) if v is not empty_node else v for k, v in flat.items()}
  )

