from typing import Optional

def from_flat_dict(
    flat_dict: PyTree,
    target: Optional[PyTree] = None,
    sep: Optional[str] = None,
    *,
    inplace: bool = False,
) -> PyTree:
  """Reconstructs the original tree object from a flattened dictionary.

  Args:
    flat_dict: A dictionary conforming to the return value of `to_flat_dict`.
    target: A reference PyTree. The returned value will conform to this
      structure. If not provided, an unflattened dict will be returned with the
      inferred structure of the original tree, without necessarily matching it
      exactly. Note, if not provided, the keys in `flat_dict` need to match
      `sep`.
    sep: separator used for nested keys in `flat_dict`.
    inplace: If True, removes items from flat_dict as they are added to the
      result.

  Returns:
    A dict matching the structure of `tree` with the values of `flat_dict`.
  """
  if inplace and not isinstance(flat_dict, dict):
    raise ValueError('Inplace operations require flat_dict to be a dict.')
  if target is None:
    # A bare top-level leaf flattens to the single empty keypath `()`; there is
    # no container to rebuild, so the value is the whole tree (mirrors
    # `from_flattened_with_keypath`).
    if sep is None and () in flat_dict:
      if len(flat_dict) != 1:
        raise ValueError(
            f'Empty keypath () must be the only key; got {list(flat_dict)}.'
        )
      return flat_dict.pop(()) if inplace else flat_dict[()]
    result = {}
    for k in list(flat_dict):
      v = flat_dict.pop(k) if inplace else flat_dict[k]
      subtree = result
      if sep is None:
        assert isinstance(k, tuple)
        tuple_k = k
      else:
        tuple_k = tuple(k.split(sep))
      for i, name in enumerate(tuple_k):
        if i == len(tuple_k) - 1:
          assert name not in subtree
          subtree[name] = v
        else:
          if name not in subtree:
            subtree[name] = {}
          subtree = subtree[name]
    return result
  else:
    flat_structure = to_flat_dict(target, sep=sep)
    # Ensure that the ordering of `flat_dict` keys matches that of `target`.
    # Necessary for later unflattening.
    ordered_keys = flat_structure.keys()
    if inplace:
      values = [flat_dict.pop(k) for k in ordered_keys]
    else:
      values = [flat_dict[k] for k in ordered_keys]
    return jax.tree.unflatten(jax.tree.structure(target), values)

