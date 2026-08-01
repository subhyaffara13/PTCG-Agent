
def treespec_leaf() -> TreeSpec:
    """Make a treespec representing a leaf node."""
    return optree.treespec_leaf(none_is_leaf=True, namespace="torch")


def treespec_leaf() -> LeafSpec:
    """Make a treespec representing a leaf node."""
    return _LEAF_SPEC


def treespec_leaf(
    *,
    none_is_leaf: bool = False,
    namespace: str = "",  # unused
) -> PyTreeSpec:
    return PyTreeSpec(
        (),
        None,
        None,
        (),
        None,
        none_is_leaf=none_is_leaf,
        namespace="",
    )

