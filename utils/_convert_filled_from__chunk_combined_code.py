
def _convert_filled_from_ChunkCombinedCode(
    filled: cpy.FillReturn_ChunkCombinedCode,
    fill_type_to: FillType,
) -> cpy.FillReturn:
    if fill_type_to == FillType.ChunkCombinedCode:
        return filled
    elif fill_type_to == FillType.ChunkCombinedOffset:
        codes = [None if codes is None else arr.offsets_from_codes(codes) for codes in filled[1]]
        return (filled[0], codes)
    else:
        raise ValueError(
            f"Conversion from {FillType.ChunkCombinedCode} to {fill_type_to} not supported")

