
def set_chunking_meta(
    node: Node, meta: ChunkingMeta | None = None, **kwargs: Any
) -> bool:
    """
    kwargs can override fields in the passed in `meta`
    """
    if meta is None:
        meta = ChunkingMeta(**kwargs)
    else:
        # make a copy to avoid override the passed in instance
        meta = meta.copy()
        for k, v in kwargs.items():
            setattr(meta, k, v)

    old_meta = get_chunking_meta(node)
    node.meta["chunking"] = meta
    return old_meta is None or old_meta != meta

