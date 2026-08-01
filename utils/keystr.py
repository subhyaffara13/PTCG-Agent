
def keystr(kp: KeyPath) -> str:
    """Given a key path, return a pretty-printed representation."""
    raise NotImplementedError("KeyPaths are not yet supported in cxx_pytree.")


def keystr(kp: KeyPath) -> str:
    """Given a key path, return a pretty-printed representation."""
    return "".join([str(k) for k in kp])


def keystr(keys: KeyPath, *, simple: bool = False, separator: str = '') -> str:
  """Helper to pretty-print a tuple of keys.

  Args:
    keys: A tuple of ``KeyEntry`` or any class that can be converted to string.
    simple: If True, use a simplified string representation for keys. The
      simple representation of keys will be more compact than the default, but
      is ambiguous in some cases (for example "0" might refer to the first item
      in a list or a dictionary key for the integer 0 or string "0").
    separator: The separator to use to join string representations of the keys.

  Returns:
    A string that joins all string representations of the keys.

  Examples:
    >>> import jax
    >>> params = {'foo': {'bar': {'baz': 1, 'bat': [2, 3]}}}
    >>> for path, _ in jax.tree_util.tree_leaves_with_path(params):
    ...   print(jax.tree_util.keystr(path))
    ['foo']['bar']['bat'][0]
    ['foo']['bar']['bat'][1]
    ['foo']['bar']['baz']
    >>> for path, _ in jax.tree_util.tree_leaves_with_path(params):
    ...   print(jax.tree_util.keystr(path, simple=True, separator='/'))
    foo/bar/bat/0
    foo/bar/bat/1
    foo/bar/baz
  """
  str_fn = _simple_entrystr if simple else str
  return separator.join(map(str_fn, keys))

