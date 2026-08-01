
def has_any_chunking_meta(*node_list: Node) -> bool:
    from .core import get_chunking_meta

    return any(get_chunking_meta(node) for node in node_list)

