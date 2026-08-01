
def _convert_lines_from_ChunkCombinedNan(
    lines: cpy.LineReturn_ChunkCombinedNan,
    line_type_to: LineType,
) -> cpy.LineReturn:
    if line_type_to in (LineType.Separate, LineType.SeparateCode):
        separate_lines = []
        for points in lines[0]:
            if points is not None:
                separate_lines += arr.split_points_at_nan(points)
        if line_type_to == LineType.Separate:
            return separate_lines
        else:
            separate_codes = [arr.codes_from_points(points) for points in separate_lines]
            return (separate_lines, separate_codes)
    elif line_type_to == LineType.ChunkCombinedCode:
        chunk_points: list[cpy.PointArray | None] = []
        chunk_codes: list[cpy.CodeArray | None] = []
        for points in lines[0]:
            if points is None:
                chunk_points.append(None)
                chunk_codes.append(None)
            else:
                points, offsets = arr.remove_nan(points)
                chunk_points.append(points)
                chunk_codes.append(arr.codes_from_offsets_and_points(offsets, points))
        return (chunk_points, chunk_codes)
    elif line_type_to == LineType.ChunkCombinedOffset:
        chunk_points = []
        chunk_offsets: list[cpy.OffsetArray | None] = []
        for points in lines[0]:
            if points is None:
                chunk_points.append(None)
                chunk_offsets.append(None)
            else:
                points, offsets = arr.remove_nan(points)
                chunk_points.append(points)
                chunk_offsets.append(offsets)
        return (chunk_points, chunk_offsets)
    elif line_type_to == LineType.ChunkCombinedNan:
        return lines
    else:
        raise ValueError(f"Invalid LineType {line_type_to}")

