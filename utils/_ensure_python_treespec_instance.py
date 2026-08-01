
def _ensure_python_treespec_instance(
    treespec: "TreeSpec | cxx_pytree.PyTreeSpec",
) -> TreeSpec:
    if isinstance(treespec, TreeSpec):
        return treespec

    if not _is_pytreespec_instance(treespec):
        raise TypeError(
            f"Expected `treespec` to be an instance of "
            f"PyTreeSpec but got item of type {type(treespec)}."
        )
    dummy_tree = treespec.unflatten([0] * treespec.num_leaves)
    return tree_structure(dummy_tree)

