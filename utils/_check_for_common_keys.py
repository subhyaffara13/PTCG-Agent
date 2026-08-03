from typing import Any, Callable

def _check_for_common_keys(
    trees: Iterable[PyTree],
    is_leaf: Callable[[Any], bool],
) -> None:
  """Checks `trees` for common keys and raises a `ValueError` if found."""
  seen_keys = set()
  for tree in trees:
    flat_tree = utils.to_flat_dict(tree, is_leaf=is_leaf)
    common_keys = seen_keys.intersection(flat_tree.keys())
    if common_keys:
      raise ValueError(
          'Found common key paths when overwrite is False: '
          f'{sorted(list(common_keys))}'
      )
    seen_keys.update(flat_tree.keys())

