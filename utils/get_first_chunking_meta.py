
def get_first_chunking_meta(*node_list: Node) -> ChunkingMeta | None:
    """
    Get the first non-none chunking metadata if there is any.
    """
    from .core import get_chunking_meta

    for node in node_list:
        if (meta := get_chunking_meta(node)) is not None:
            return meta

    return None

