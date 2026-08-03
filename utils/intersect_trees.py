from typing import Optional

def intersect_trees(*trees: PyTree, target: Optional[PyTree] = None) -> PyTree:
  """Intersects the provided trees, dropping any keys not in common between all.

  For overlapping keys, the key of the last tree in the list will take
  precedence.

  Args:
    *trees: PyTrees to intersect.
    target: A PyTree to provide structure for the returned value. If not
      provided, the result will take the form of a dictionary.

  Returns:
    A single intersected PyTree.
  """
  trees = [tree_utils.to_flat_dict(t) for t in trees]
  tree_keys = set.intersection(*[set(t.keys()) for t in trees])
  return tree_utils.from_flat_dict(
      {k: trees[-1][k] for k in tree_keys}, target=target
  )

