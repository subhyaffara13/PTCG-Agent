from typing import Any

def treespec_dict(
    mapping: Mapping[Any, TreeSpec] | Iterable[tuple[Any, TreeSpec]] = (),
    /,
    **kwargs: TreeSpec,
) -> TreeSpec:
    """Make a dict treespec from a dict of child treespecs."""
    return optree.treespec_dict(
        mapping,
        **kwargs,
        none_is_leaf=True,
        namespace="torch",
    )


def treespec_dict(
    mapping: Mapping[Any, TreeSpec] | Iterable[tuple[Any, TreeSpec]] = (),
    /,
    **kwargs: TreeSpec,
) -> TreeSpec:
    """Make a dict treespec from a dict of child treespecs."""
    dct = dict(mapping, **kwargs)
    if any(not isinstance(child, TreeSpec) for child in dct.values()):
        raise ValueError(f"Expected a dictionary of TreeSpec values, got: {dct!r}.")
    return TreeSpec(dict, list(dct.keys()), list(dct.values()))


def treespec_dict(
    mapping: Mapping[Any, PyTreeSpec] | Iterable[tuple[Any, PyTreeSpec]] = (),
    /,
    *,
    none_is_leaf: bool = False,
    namespace: str = "",
    **kwargs: PyTreeSpec,
) -> PyTreeSpec:
    dct = dict(mapping, **kwargs)
    if any(not _is_pytreespec_instance(child) for child in dct.values()):
        raise ValueError(f"Expected a dictionary of TreeSpecs, got: {dct!r}.")
    if any(child.none_is_leaf != none_is_leaf for child in dct.values()):
        raise ValueError(
            "All children PyTreeSpecs must have the same `none_is_leaf` value "
            f"as the parent; expected {none_is_leaf}, got: {dct!r}.",
        )
    if any(child.namespace not in (namespace, "") for child in dct.values()):
        raise ValueError(
            "All children PyTreeSpecs must have the same `namespace` value "
            f"as the parent; expected {namespace!r}, got: {dct!r}.",
        )

    (
        children,
        metadata,
        entries,
        unflatten_func,
    ) = optree.tree_flatten_one_level(  # type: ignore[assignment,var-annotated]
        dct,  # type: ignore[arg-type]
        none_is_leaf=none_is_leaf,
        namespace=namespace,
    )
    return PyTreeSpec(
        tuple(children),  # type: ignore[arg-type]
        dict,
        metadata,
        entries,
        unflatten_func,  # type: ignore[arg-type]
        none_is_leaf=none_is_leaf,
        namespace=namespace,
    )

