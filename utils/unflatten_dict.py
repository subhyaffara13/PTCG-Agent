
def unflatten_dict(xs, sep=None):
  """Unflatten a dictionary.

  See ``flatten_dict``

  Example::

    >>> flat_xs = {
    ...   ('foo',): 1,
    ...   ('bar', 'a'): 2,
    ... }
    >>> xs = unflatten_dict(flat_xs)
    >>> xs
    {'foo': 1, 'bar': {'a': 2}}

  Args:
    xs: a flattened dictionary
    sep: separator (same as used with ``flatten_dict()``).
  Returns:
    The nested dictionary.
  """
  assert isinstance(xs, dict), f'input is not a dict; it is a {type(xs)}'
  result = {}
  for path, value in xs.items():
    if sep is not None:
      path = path.split(sep)
    if value is empty_node:
      value = {}
    cursor = result
    for key in path[:-1]:
      if key not in cursor:
        cursor[key] = {}
      cursor = cursor[key]
    cursor[path[-1]] = value
  return result

