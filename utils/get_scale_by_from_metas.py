
def get_scale_by_from_metas(*metas: ChunkingMeta) -> Node | None:
    """
    If there are multiple ChunkingMeta having the scale_by field,
    raise a CantChunk exception.

    If no ChunkingMeta has scale_by field, return None.
    Other wise return the only scale_by field.
    """

    scale_by_list = []

    # don't do dedup on the scale_by field on purpose for this API
    for meta in metas:
        if meta.scale_by is not None:
            scale_by_list.append(meta.scale_by)

    if len(scale_by_list) > 1:
        raise CantChunk("Multiple scale_by")

    return scale_by_list[0] if len(scale_by_list) == 1 else None

