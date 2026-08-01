
def update_chunking_meta(node: Node, **kwargs: Any) -> bool:
    """
    Unlike set_chunking_mete, this function keeps the existing chunking
    metadata if it's not overridden.
    """
    changed = False
    meta = get_chunking_meta(node)
    if meta is None:
        meta = ChunkingMeta()
        changed = True
    for k, v in kwargs.items():
        if getattr(meta, k, None) != v:
            changed = True
            setattr(meta, k, v)

    node.meta["chunking"] = meta
    return changed

