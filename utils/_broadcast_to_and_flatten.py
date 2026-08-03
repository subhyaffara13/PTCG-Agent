from typing import Any, Callable

def _broadcast_to_and_flatten(
    tree: PyTree,
    treespec: TreeSpec,
    is_leaf: Callable[[PyTree], bool] | None = None,
) -> list[Any] | None:
    if not _is_pytreespec_instance(treespec):
        raise TypeError(
            f"Expected `treespec` to be an instance of "
            f"PyTreeSpec but got item of type {type(treespec)}."
        )
    full_tree = tree_unflatten([0] * treespec.num_leaves, treespec)
    try:
        return broadcast_prefix(tree, full_tree, is_leaf=is_leaf)
    except ValueError:
        return None


def _broadcast_to_and_flatten(
    tree: PyTree,
    treespec: TreeSpec,
    is_leaf: Callable[[PyTree], bool] | None = None,
) -> list[Any] | None:
    def broadcast_prefix(
        prefix_tree: PyTree,
        full_tree: PyTree,
        is_leaf: Callable[[PyTree], bool] | None = None,
    ) -> list[Any]:
        result: list[Any] = []

        def add_leaves(x: Any, subtree: PyTree) -> None:
            subtreespec = tree_structure(subtree, is_leaf=is_leaf)
            result.extend([x] * subtreespec.num_leaves)

        tree_map_(
            add_leaves,
            prefix_tree,
            full_tree,
            is_leaf=is_leaf,
        )
        return result

    full_tree = tree_unflatten([0] * treespec.num_leaves, treespec)
    try:
        return broadcast_prefix(tree, full_tree, is_leaf=is_leaf)
    except ValueError:
        return None

