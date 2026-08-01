
def _convert_filled_from_ChunkCombinedOffsetOffset(
    filled: cpy.FillReturn_ChunkCombinedOffsetOffset,
    fill_type_to: FillType,
) -> cpy.FillReturn:
    if fill_type_to == FillType.OuterCode:
        separate_points = []
        separate_codes = []
        for points, offsets, outer_offsets in zip(*filled):
            if points is not None:
                if TYPE_CHECKING:
                    assert offsets is not None
                    assert outer_offsets is not None
                codes = arr.codes_from_offsets_and_points(offsets, points)
                outer_offsets = offsets[outer_offsets]
                separate_points += arr.split_points_by_offsets(points, outer_offsets)
                separate_codes += arr.split_codes_by_offsets(codes, outer_offsets)
        return (separate_points, separate_codes)
    elif fill_type_to == FillType.OuterOffset:
        separate_points = []
        separate_offsets = []
        for points, offsets, outer_offsets in zip(*filled):
            if points is not None:
                if TYPE_CHECKING:
                    assert offsets is not None
                    assert outer_offsets is not None
                if len(outer_offsets) > 2:
                    separate_offsets += [offsets[s:e+1] - offsets[s] for s, e in
                                         pairwise(outer_offsets)]
                else:
                    separate_offsets.append(offsets)
                separate_points += arr.split_points_by_offsets(points, offsets[outer_offsets])
        return (separate_points, separate_offsets)
    elif fill_type_to == FillType.ChunkCombinedCode:
        chunk_codes: list[cpy.CodeArray | None] = []
        for points, offsets, outer_offsets in zip(*filled):
            if points is None:
                chunk_codes.append(None)
            else:
                if TYPE_CHECKING:
                    assert offsets is not None
                    assert outer_offsets is not None
                chunk_codes.append(arr.codes_from_offsets_and_points(offsets, points))
        ret1: cpy.FillReturn_ChunkCombinedCode = (filled[0], chunk_codes)
        return ret1
    elif fill_type_to == FillType.ChunkCombinedOffset:
        return (filled[0], filled[1])
    elif fill_type_to == FillType.ChunkCombinedCodeOffset:
        chunk_codes = []
        chunk_outer_offsets: list[cpy.OffsetArray | None] = []
        for points, offsets, outer_offsets in zip(*filled):
            if points is None:
                chunk_codes.append(None)
                chunk_outer_offsets.append(None)
            else:
                if TYPE_CHECKING:
                    assert offsets is not None
                    assert outer_offsets is not None
                chunk_codes.append(arr.codes_from_offsets_and_points(offsets, points))
                chunk_outer_offsets.append(offsets[outer_offsets])
        ret2: cpy.FillReturn_ChunkCombinedCodeOffset = (filled[0], chunk_codes, chunk_outer_offsets)
        return ret2
    elif fill_type_to == FillType.ChunkCombinedOffsetOffset:
        return filled
    else:
        raise ValueError(f"Invalid FillType {fill_type_to}")

