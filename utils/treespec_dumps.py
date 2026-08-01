
def treespec_dumps(treespec: TreeSpec, protocol: int | None = None) -> str:
    """Serialize a treespec to a JSON string."""
    if not _is_pytreespec_instance(treespec):
        raise TypeError(
            f"Expected `treespec` to be an instance of "
            f"PyTreeSpec but got item of type {type(treespec)}."
        )

    dummy_tree = tree_unflatten([0] * treespec.num_leaves, treespec)
    orig_treespec = python_pytree.tree_structure(dummy_tree)
    return python_pytree.treespec_dumps(orig_treespec, protocol=protocol)


def treespec_dumps(treespec: TreeSpec, protocol: int | None = None) -> str:
    treespec = _ensure_python_treespec_instance(treespec)

    if protocol is None:
        protocol = DEFAULT_TREESPEC_SERIALIZATION_PROTOCOL

    if protocol in _SUPPORTED_PROTOCOLS:
        json_spec = _SUPPORTED_PROTOCOLS[protocol].treespec_to_json(treespec)
    else:
        raise ValueError(
            f"Unknown protocol {protocol}. "
            f"Available protocols: {list(_SUPPORTED_PROTOCOLS.keys())}",
        )

    str_spec = json.dumps((protocol, dataclasses.asdict(json_spec)), cls=EnumEncoder)
    return str_spec

