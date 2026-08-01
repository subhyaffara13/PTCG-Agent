
def flatten_mapping(xs: Mapping[Any, Any],
                    /,
                    *,
                    keep_empty_nodes: bool = False,
                    is_leaf: None | IsLeafCallable = None,
                    sep: None = None
                    ) -> dict[tuple[Any, ...], Any]:
  ...


def flatten_mapping(xs: Mapping[Any, Any],
                    /,
                    *,
                    keep_empty_nodes: bool = False,
                    is_leaf: None | IsLeafCallable = None,
                    sep: str,
                    ) -> dict[str, Any]:
  ...


def flatten_mapping(xs: Mapping[Any, Any],
                    /,
                    *,
                    keep_empty_nodes: bool = False,
                    is_leaf: None | IsLeafCallable = None,
                    sep: None | str = None
                    ) -> dict[Any, Any]:
  """Flatten a nested mapping.

  The nested keys are flattened to a tuple. See ``unflatten_mapping`` on how to
  restore the nested mapping.

  Example::

    >>> from flax import nnx
    >>> xs = {'foo': 1, 'bar': {'a': 2, 'b': {}}}
    >>> flat_xs = nnx.traversals.flatten_mapping(xs)
    >>> flat_xs
    {('foo',): 1, ('bar', 'a'): 2}

  Note that empty mappings are ignored and will not be restored by
  ``unflatten_mapping``.

  Args:
    xs: a nested mapping
    keep_empty_nodes: replaces empty mappings with
      ``traverse_util.empty_node``.
    is_leaf: an optional function that takes the next nested mapping and nested
      keys and returns True if the nested mapping is a leaf (i.e., should not be
      flattened further).
    sep: if specified, then the keys of the returned mapping will be
      ``sep``-joined strings (if ``None``, then keys will be tuples).
  Returns:
    The flattened mapping.
  """
  assert isinstance(
    xs, Mapping
  ), f'expected Mapping; got {type(xs).__qualname__}'

  def _key(path: tuple[Any, ...]) -> tuple[Any, ...] | str:
    if sep is None:
      return path
    return sep.join(path)

  def _flatten(xs: Any, prefix: tuple[Any, ...]) -> dict[Any, Any]:
    if not isinstance(xs, Mapping) or (
      is_leaf and is_leaf(prefix, xs)
    ):
      return {_key(prefix): xs}
    result = {}
    is_empty = True
    for key, value in xs.items():
      is_empty = False
      path = prefix + (key,)
      result.update(_flatten(value, path))
    if keep_empty_nodes and is_empty:
      if prefix == ():  # when the whole input is empty
        return {}
      return {_key(prefix): empty_node}
    return result

  return _flatten(xs, ())

