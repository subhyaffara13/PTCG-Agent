
def get_scale_by_from_node(node: Node) -> Node | None:
    from .core import get_chunking_meta

    meta = get_chunking_meta(node)
    return meta.scale_by if meta is not None else None

