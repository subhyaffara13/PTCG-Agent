
def equality_errors_pytreedef(
    tree1: PyTreeDef,
    tree2: PyTreeDef) -> Iterable[tuple[KeyPath, str, str, str]]:
  """Like `equality_errors` but invoked on PyTreeDef."""
  # TODO(mattjj): make equality_errors not print type name, avoid metaclass
  leaf = type("LeafMeta", (type,), dict(__repr__=lambda _: "pytree leaf")
              )("Leaf", (), {})()
  return equality_errors(tree_unflatten(tree1, [leaf] * tree1.num_leaves),
                         tree_unflatten(tree2, [leaf] * tree2.num_leaves))

