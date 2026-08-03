from typing import Callable

def _is_leaf(tree: PyTree, is_leaf: Callable[[PyTree], bool] | None = None) -> bool:
    return tree_is_leaf(tree, is_leaf=is_leaf)

