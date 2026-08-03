from typing import Any, Callable

def unravel_pytree(
  treedef: PyTreeDef,
  unravel_list: Callable[[Array], Iterable[Leaf]],
  flat: Array,
) -> Any:
  return tree_unflatten(treedef, unravel_list(flat))

