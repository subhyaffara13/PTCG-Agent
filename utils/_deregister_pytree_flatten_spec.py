
def _deregister_pytree_flatten_spec(
    cls: type[Any],
) -> None:
    del SUPPORTED_NODES[cls]
    del SUPPORTED_NODES_EXACT_MATCH[cls]

