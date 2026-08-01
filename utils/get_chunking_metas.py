
def get_chunking_metas(
    nodes: Sequence[Node], skip_none: bool = False
) -> Sequence[ChunkingMeta | None]:
    return [
        get_chunking_meta(node)
        for node in nodes
        if not skip_none or get_chunking_meta(node) is not None
    ]

