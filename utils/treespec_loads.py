
def treespec_loads(serialized: str) -> TreeSpec:
    """Deserialize a treespec from a JSON string."""
    orig_treespec = python_pytree.treespec_loads(serialized)
    dummy_tree = python_pytree.tree_unflatten(
        [0] * orig_treespec.num_leaves,
        orig_treespec,
    )
    treespec = tree_structure(dummy_tree)
    return treespec


def treespec_loads(serialized: str) -> TreeSpec:
    protocol, json_schema = json.loads(serialized)

    if protocol in _SUPPORTED_PROTOCOLS:
        return _SUPPORTED_PROTOCOLS[protocol].json_to_treespec(json_schema)
    raise ValueError(
        f"Unknown protocol {protocol}. "
        f"Available protocols: {list(_SUPPORTED_PROTOCOLS.keys())}",
    )

