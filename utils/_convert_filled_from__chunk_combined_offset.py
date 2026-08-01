
def _convert_filled_from_ChunkCombinedOffset(
    filled: cpy.FillReturn_ChunkCombinedOffset,
    fill_type_to: FillType,
) -> cpy.FillReturn:
    if fill_type_to == FillType.ChunkCombinedCode:
        chunk_codes: list[cpy.CodeArray | None] = []
        for points, offsets in zip(*filled):
            if points is None:
                chunk_codes.append(None)
            else:
                if TYPE_CHECKING:
                    assert offsets is not None
                chunk_codes.append(arr.codes_from_offsets_and_points(offsets, points))
        return (filled[0], chunk_codes)
    elif fill_type_to == FillType.ChunkCombinedOffset:
        return filled
    else:
        raise ValueError(
            f"Conversion from {FillType.ChunkCombinedOffset} to {fill_type_to} not supported")

