
def flatten_dict(xs, keep_empty_nodes=False, is_leaf=None, sep=None):
  """Flatten a nested dictionary.

  The nested keys are flattened to a tuple.
  See ``unflatten_dict`` on how to restore the
  nested dictionary structure.

  Example::

    >>> from flax.traverse_util import flatten_dict

    >>> xs = {'foo': 1, 'bar': {'a': 2, 'b': {}}}
    >>> flat_xs = flatten_dict(xs)
    >>> flat_xs
    {('foo',): 1, ('bar', 'a'): 2}

  Note that empty dictionaries are ignored and
  will not be restored by ``unflatten_dict``.

  Args:
    xs: a nested dictionary
    keep_empty_nodes: replaces empty dictionaries
      with ``traverse_util.empty_node``.
    is_leaf: an optional function that takes the
      next nested dictionary and nested keys and
      returns True if the nested dictionary is a
      leaf (i.e., should not be flattened further).
    sep: if specified, then the keys of the returned
      dictionary will be ``sep``-joined strings (if
      ``None``, then keys will be tuples).
  Returns:
    The flattened dictionary.
  """
  assert isinstance(
    xs, (flax.core.FrozenDict, dict)
  ), f'expected (frozen)dict; got {type(xs)}'

  return _flatten(xs, (), keep_empty_nodes, is_leaf, sep)


def flatten_dict(d: MutableMapping, parent_key: str = "", delimiter: str = "."):
    """Flatten a nested dict into a single level dict."""

    def _flatten_dict(d, parent_key="", delimiter="."):
        for k, v in d.items():
            key = str(parent_key) + delimiter + str(k) if parent_key else k
            if v and isinstance(v, MutableMapping):
                yield from flatten_dict(v, key, delimiter=delimiter).items()
            else:
                yield key, v

    return dict(_flatten_dict(d, parent_key, delimiter))

