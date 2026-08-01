
def has_data(value: tp.Any, /) -> list[tp.Any]:
  visited: set[int] = set()
  def _is_leaf(x):
    if id(x) in visited:
      return True
    visited.add(id(x))
    return is_data(x)
  leaves = jax.tree.leaves(value, is_leaf=_is_leaf)
  return [leaf for leaf in leaves if is_data(leaf)]

