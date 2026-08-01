
def _visit_leaf(hint: TypeForm, leaf_fn: _LeafFn):
  """Leaf node."""
  if hint == _NoneType:  # Normalize `None`
    hint = None
  return leaf_fn(hint)

