
def lines_to_bokeh(
    lines: LineReturn,
    line_type: LineType,
) -> tuple[CoordinateArray | None, CoordinateArray | None]:
    lines = convert_lines(lines, line_type, LineType.ChunkCombinedNan)
    lines = dechunk_lines(lines, LineType.ChunkCombinedNan)
    if TYPE_CHECKING:
        lines = cast(LineReturn_ChunkCombinedNan, lines)
    points = lines[0][0]
    if points is None:
        return None, None
    else:
        return points[:, 0], points[:, 1]

