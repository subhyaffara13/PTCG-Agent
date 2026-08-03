from typing import Any

def _get_node_type(tree: Any) -> Any:
    node_type = type(tree)
    # All namedtuple types are implicitly registered as pytree nodes.
    # XXX: Other parts of the codebase expect namedtuple types always return
    #      `namedtuple` instead of the actual namedtuple type. Even if the type
    #      is explicitly registered.
    if is_namedtuple_class(node_type):
        return namedtuple
    return node_type

