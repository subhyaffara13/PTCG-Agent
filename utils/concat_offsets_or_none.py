
def concat_offsets_or_none(
    list_of_offsets_or_none: list[cpy.OffsetArray | None],
) -> cpy.OffsetArray | None:
    """Concatenate a list of offsets arrays or None into a single offset array or None.
    """
    list_of_offsets = [offsets for offsets in list_of_offsets_or_none if offsets is not None]
    if list_of_offsets:
        return concat_offsets(list_of_offsets)
    else:
        return None

