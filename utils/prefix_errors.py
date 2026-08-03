from typing import Any, Callable

def prefix_errors(prefix_tree: Any, full_tree: Any,
                  is_leaf: Callable[[Any], bool] | None = None,
                  ) -> list[Callable[[str], ValueError]]:
  return list(_prefix_error((), prefix_tree, full_tree, is_leaf))

