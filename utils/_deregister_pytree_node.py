from typing import Any

def _deregister_pytree_node(
    cls: type[Any],
) -> None:
    """This is an internal function that is used to deregister a pytree node type
    for the Python pytree only. This should be only used inside PyTorch.
    """
    with _NODE_REGISTRY_LOCK:
        del SUPPORTED_NODES[cls]
        node_def = SUPPORTED_SERIALIZED_TYPES[cls]
        del SERIALIZED_TYPE_TO_PYTHON_TYPE[node_def.serialized_type_name]
        del SUPPORTED_SERIALIZED_TYPES[cls]
        CONSTANT_NODES.discard(cls)

