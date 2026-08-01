
def _C_flatten(
    tree: PyTree,
    /,
    leaf_predicate: Callable[[PyTree], bool] | None = None,
    none_is_leaf: bool = False,
    namespace: str = "",
) -> tuple[list[Any], PyTreeSpec]:
    return tree_flatten(  # type: ignore[return-value]
        tree,
        is_leaf=leaf_predicate,
        none_is_leaf=none_is_leaf,
        namespace=namespace,
    )

