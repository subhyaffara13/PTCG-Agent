import functools
from typing import Any, Callable, Optional

def merge_trees(*trees: PyTree, target: Optional[PyTree] = None) -> PyTree:
  """Merges the provided PyTrees into a single result.

  If trees have overlapping keys, the key of the last tree in the list will take
  precedence.

  Args:
    *trees: PyTrees to merge.
    target: A PyTree to provide structure for the returned value. If not
      provided, the result will take the form of a dictionary.

  Returns:
    A single merged PyTree.
  """
  trees = [tree_utils.to_flat_dict(t) for t in trees]
  merged = functools.reduce(operator.ior, trees, {})
  return tree_utils.from_flat_dict(merged, target=target)


def merge_trees(
    *trees: PyTree,
    overwrite: bool = False,
    is_leaf: Callable[[Any], bool] | None = None,
) -> PyTree:
  """Merges trees into a single tree using a comprehensive recursive strategy.

  This implementation handles standard Python containers (dicts, lists, tuples),
  named tuples, and custom JAX PyTree nodes, mirroring the robustness of
  utilities like `tree_trim`.

  - Mappings (dict, etc.) are merged by key.
  - Sequences (list, tuple) are merged element-wise if they have the same
    length; otherwise, a ValueError is raised.
  - Dataclasses (dataclass, etc.) are merged by field name, where non-None
    values overwrite None values.
  - If `overwrite` is False, a ValueError is raised for mismatched types.

  Example:
    Merge two PyTrees without overlapping leaf paths::

      tree1 = {"a": 1, "b": {"c": 2}}
      tree2 = {"d": 3, "b": {"e": 4}}

      merged_tree = merge(tree1, tree2)
      # Result: {"a": 1, "b": {"c": 2, "e": 4}, "d": 3}

    Merge PyTrees with overlapping leaf paths using `overwrite=True`::

      tree3 = {"a": 100}
      overwritten_tree = merge(tree1, tree3, overwrite=True)
      # Result: {"a": 100, "b": {"c": 2}}

  Args:
    *trees: The trees to merge.
    overwrite: If True, later values from `trees` will overwrite earlier values
      where leaf paths conflict. If False, a ValueError is raised for
      conflicting leaves.
    is_leaf: Optional function to determine if a node is a leaf. Defaults to
      `jax.tree_util.all_leaves`.

  Returns:
    A new PyTree representing the merged content of `trees`.

  Raises:
    ValueError: If `overwrite` is False and there are common leaf key paths
      between `trees`. Or if `overwrite` is False and the types of nodes do not
      match.
  """
  is_leaf_fn = is_leaf or utils.is_leaf_node_or_none
  trees = list(trees)
  if not trees:
    return {}

  if not overwrite:
    _check_for_common_keys(trees, is_leaf_fn)

  return functools.reduce(
      lambda acc, t: _recursive_merge(t, acc, overwrite, is_leaf_fn),
      trees,
  )

