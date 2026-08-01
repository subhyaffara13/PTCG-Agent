
def has_nop_chunking_meta(node: Node) -> bool:
    return ChunkingMeta.is_nop(get_chunking_meta(node))

