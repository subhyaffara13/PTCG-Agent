
def zip_dict(  # pytype: disable=invalid-annotation
    *dicts: Unpack[dict[_KeyT, _ValuesT]],
) -> Iterator[_KeyT, tuple[Unpack[_ValuesT]]]:
  """Iterate over items of dictionaries grouped by their keys.

  Example:

  ```python
  d0 = {'a': 1, 'b': 2}
  d1 = {'a': 10, 'b': 20}
  d2 = {'a': 100, 'b': 200}

  list(epy.zip_dict(d0, d1, d2)) == [
      ('a', (1, 10, 100)),
      ('b', (2, 20, 200)),
  ]
  ```

  Args:
    *dicts: The dict to iterate over. Should all have the same keys

  Yields:
    The iterator of `(key, zip(*values))`

  Raises:
    KeyError: If dicts does not contain the same keys.
  """
  # Set does not keep order like dict, so only use set to compare keys
  all_keys = set(itertools.chain(*dicts))
  d0 = dicts[0]

  if len(all_keys) != len(d0):
    raise KeyError(f'Missing keys: {all_keys ^ set(d0)}')

  for key in d0:  # set merge all keys
    # Will raise KeyError if the dict don't have the same keys
    yield key, tuple(d[key] for d in dicts)

