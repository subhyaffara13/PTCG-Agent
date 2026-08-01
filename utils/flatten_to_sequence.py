
def flatten_to_sequence(
  xs: Mapping[Any, Any],
  /,
  *,
  is_leaf: IsLeafCallable | None = None,
) -> list[tuple[Any, Any]]:
  """Flatten a nested mapping.

  The nested keys are flattened to a tuple. See ``unflatten_mapping`` on how to
  restore the nested mapping.

  Example::

    >>> from flax import nnx
    >>> xs = {'foo': 1, 'bar': {'a': 2, 'b': {}}}
    >>> flat_xs = nnx.traversals.flatten_to_sequence(xs)
    >>> flat_xs
    [(('foo',), 1), (('bar', 'a'), 2)]

  Note that empty mappings are ignored and will not be restored by
  ``unflatten_mapping``.

  Args:
    xs: a nested mapping
    is_leaf: an optional function that takes the next nested mapping and nested
      keys and returns True if the nested mapping is a leaf (i.e., should not be
      flattened further).

  Returns:
    The flattened mapping.
  """
  assert isinstance(
    xs, Mapping
  ), f'expected Mapping; got {type(xs).__qualname__}'
  result = []

  def _flatten(xs: Any, prefix: tuple[Any, ...]):
    if not isinstance(xs, Mapping) or (is_leaf and is_leaf(prefix, xs)):
      result.append((prefix, xs))
    else:
      for key, value in xs.items():
        _flatten(value, (*prefix, key))

  _flatten(xs, ())
  return result

