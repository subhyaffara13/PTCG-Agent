from typing import Any, Callable

def _C_flatten_with_path(
    tree: PyTree,
    /,
    leaf_predicate: Callable[[PyTree], bool] | None = None,
    none_is_leaf: bool = False,
    namespace: str = "",
) -> tuple[list[tuple[Any, ...]], list[Any], PyTreeSpec]:
    return tree_flatten_with_path(  # type: ignore[return-value]
        tree,
        is_leaf=leaf_predicate,
        none_is_leaf=none_is_leaf,
        namespace=namespace,
    )

