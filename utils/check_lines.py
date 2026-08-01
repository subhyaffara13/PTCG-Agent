
def check_lines(lines: cpy.LineReturn, line_type: LineType | str) -> None:
    line_type = as_line_type(line_type)

    if line_type == LineType.Separate:
        if TYPE_CHECKING:
            lines = cast(cpy.LineReturn_Separate, lines)
        if not isinstance(lines, list):
            raise TypeError(f"Expected list not {type(lines)}")
        for points in lines:
            check_point_array(points)
    elif line_type == LineType.SeparateCode:
        if TYPE_CHECKING:
            lines = cast(cpy.LineReturn_SeparateCode, lines)
        _check_tuple_of_lists_with_same_length(lines, 2)
        for i, (points, codes) in enumerate(zip(*lines)):
            check_point_array(points)
            check_code_array(codes)
            if len(points) != len(codes):
                raise ValueError(f"Points and codes have different lengths in line {i}")
    elif line_type == LineType.ChunkCombinedCode:
        if TYPE_CHECKING:
            lines = cast(cpy.LineReturn_ChunkCombinedCode, lines)
        _check_tuple_of_lists_with_same_length(lines, 2, allow_empty_lists=False)
        for chunk, (points_or_none, codes_or_none) in enumerate(zip(*lines)):
            if points_or_none is not None and codes_or_none is not None:
                check_point_array(points_or_none)
                check_code_array(codes_or_none)
                if len(points_or_none) != len(codes_or_none):
                    raise ValueError(f"Points and codes have different lengths in chunk {chunk}")
            elif not (points_or_none is None and codes_or_none is None):
                raise ValueError(f"Inconsistent Nones in chunk {chunk}")
    elif line_type == LineType.ChunkCombinedOffset:
        if TYPE_CHECKING:
            lines = cast(cpy.LineReturn_ChunkCombinedOffset, lines)
        _check_tuple_of_lists_with_same_length(lines, 2, allow_empty_lists=False)
        for chunk, (points_or_none, offsets_or_none) in enumerate(zip(*lines)):
            if points_or_none is not None and offsets_or_none is not None:
                check_point_array(points_or_none)
                check_offset_array(offsets_or_none)
                if offsets_or_none[-1] != len(points_or_none):
                    raise ValueError(f"Inconsistent points and offsets in chunk {chunk}")
            elif not (points_or_none is None and offsets_or_none is None):
                raise ValueError(f"Inconsistent Nones in chunk {chunk}")
    elif line_type == LineType.ChunkCombinedNan:
        if TYPE_CHECKING:
            lines = cast(cpy.LineReturn_ChunkCombinedNan, lines)
        _check_tuple_of_lists_with_same_length(lines, 1, allow_empty_lists=False)
        for _chunk, points_or_none in enumerate(lines[0]):
            if points_or_none is not None:
                check_point_array(points_or_none)
    else:
        raise ValueError(f"Invalid LineType {line_type}")

