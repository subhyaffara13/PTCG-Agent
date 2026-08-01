
def unflatten_mapping(
    xs: Sequence[tuple[tuple[Any, ...], Any]], /, *, sep: None = None
) -> dict[Any, Any]:
  ...


def unflatten_mapping(
    xs: Mapping[tuple[Any, ...], Any], /, *, sep: None = None
) -> dict[Any, Any]:
  ...


def unflatten_mapping(xs: Mapping[str, Any], /, *, sep: str) -> dict[Any, Any]:
  ...


def unflatten_mapping(xs: Any, /, *, sep: str | None = None) -> dict[Any, Any]:
  """Unflatten a mapping.

  See ``flatten_mapping``

  Example::

    >>> from flax import nnx
    >>> flat_xs = {
    ...   ('foo',): 1,
    ...   ('bar', 'a'): 2,
    ... }
    >>> xs = nnx.traversals.unflatten_mapping(flat_xs)
    >>> xs
    {'foo': 1, 'bar': {'a': 2}}

  Args:
    xs: a flattened mapping.
    sep: separator (same as used with ``flatten_mapping()``).
  Returns:
    The nested mapping.
  """
  if isinstance(xs, Mapping):
    xs = xs.items()

  if not isinstance(xs, Iterable):
    raise TypeError(
      f'expected Mapping or Iterable; got {type(xs).__qualname__}'
    )
  result: dict[Any, Any] = {}
  for path, value in xs:
    if sep is not None:
      path = path.split(sep)  # type: ignore
    if value is empty_node:
      value = {}
    cursor = result
    for key in path[:-1]:
      if key not in cursor:
        cursor[key] = {}
      cursor = cursor[key]
    cursor[path[-1]] = value
  return result

