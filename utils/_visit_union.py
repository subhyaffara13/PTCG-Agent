
def _visit_union(hint: TypeForm, leaf_fn: _LeafFn):
  """Recurse in `Union[x, y]`, `x | y`, or `Optional[x]`."""
  item_hints = typing_extensions.get_args(hint)
  for item_hint in item_hints:
    visit(item_hint, leaf_fn)

