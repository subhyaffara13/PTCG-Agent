from typing import Optional

def tree_cast(
    tree: base.ArrayTree, dtype: Optional[jax.typing.DTypeLike]
) -> base.ArrayTree:
  """Cast tree to given dtype, skip if None.

  Args:
    tree: the tree to cast.
    dtype: the dtype to cast to, or None to skip.

  Returns:
    the tree, with leaves cast to dtype.

  Examples:
    >>> import jax.numpy as jnp
    >>> import optax
    >>> tree = {'a': {'b': jnp.array(1.0, dtype=jnp.float32)},
    ...         'c': jnp.array(2.0, dtype=jnp.float32)}
    >>> optax.tree_utils.tree_cast(tree, dtype=jnp.bfloat16)
    {'a': {'b': Array(1, dtype=bfloat16)}, 'c': Array(2, dtype=bfloat16)}
  """
  if dtype is not None:
    return jax.tree.map(lambda t: t.astype(dtype), tree)
  else:
    return tree

