from typing import Any

def tree_size(tree: Any) -> int:
  r"""Total size of a pytree.

  Args:
    tree: pytree

  Returns:
    the total size of the pytree.
  """
  return sum(jnp.size(leaf) for leaf in jax.tree.leaves(tree))

