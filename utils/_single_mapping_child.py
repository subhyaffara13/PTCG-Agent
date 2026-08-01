
def _single_mapping_child(tree: PyTree) -> Any | None:
  if isinstance(tree, Mapping) and len(tree) == 1:
    return next(iter(tree.values()))
  return None

