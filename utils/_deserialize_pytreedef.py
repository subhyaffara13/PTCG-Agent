import itertools
from typing import Any

def _deserialize_pytreedef(
    p: ser_flatbuf.PyTreeDef,
    py_tree_leaves: Sequence[Any] | None = None,
) -> tree_util.PyTreeDef:
  # We construct a PyTree and later we'll flatten it to get the PyTreeDef.
  # In some cases the placeholder can cause issues when building the PyTree
  # (e.g. if some custom objects in the tree expect array-like leaves with
  # specific dims). To support these cases we allow passing the actual leaves.
  # TODO: is there a more direct way to construct a PyTreeDef without having to
  # construct the PyTree? (which would avoid the need for leaves).
  if py_tree_leaves is not None:
    leaf_iterator = iter(py_tree_leaves)
  else:
    # 0.0 placeholder if no leaves are provided.
    leaf_iterator = itertools.repeat(0.0)
  pytree = _deserialize_pytreedef_to_pytree(p, leaf_iterator)
  if py_tree_leaves is not None:
    assert not (list(leaf_iterator))  # Should be exhausted.
  return tree_util.tree_structure(pytree)

