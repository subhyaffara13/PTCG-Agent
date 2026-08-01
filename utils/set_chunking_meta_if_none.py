
def set_chunking_meta_if_none(
    nodes: Sequence[Node],
    meta: ChunkingMeta,
    filter_for_nop: Callable[[Node], bool] | None = None,
) -> bool:
    """
    If filter_fop_nop returns true for a node, we set the chunking
    meta to nop instead.
    """
    changed = False
    for node in nodes:
        if get_chunking_meta(node) is None:
            changed = True
            if filter_for_nop and filter_for_nop(node):
                set_chunking_meta(node)
            else:
                set_chunking_meta(node, meta)
    return changed

