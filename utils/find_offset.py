
def find_offset(
    offset: int, mapping: processor._LogicalMapping
) -> tuple[int, int]:
    """Find the offset tuple for a single offset."""
    if isinstance(offset, tuple):
        return offset

    for token in mapping:
        token_offset = token[0]
        if offset <= token_offset:
            position = token[1]
            break
    else:
        position = (0, 0)
        offset = token_offset = 0
    return (position[0], position[1] + offset - token_offset)

