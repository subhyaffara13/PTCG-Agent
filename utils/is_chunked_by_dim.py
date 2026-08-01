
def is_chunked_by_dim(node: Node, dim: int) -> bool:
    from .core import get_chunking_meta

    meta = get_chunking_meta(node)
    return meta is not None and meta.chunked_by_dim(dim)

