
def convert_multi_lines(
    multi_lines: list[cpy.LineReturn],
    line_type_from: LineType | str,
    line_type_to:  LineType | str,
) -> list[cpy.LineReturn]:
    """Convert multiple sets of contour lines from one :class:`~.LineType` to another.

    Args:
        multi_lines (nested sequence of arrays): Contour lines to convert, such as those returned by
            :meth:`.ContourGenerator.multi_lines`.
        line_type_from (LineType or str): :class:`~.LineType` to convert from as enum or
            string equivalent.
        line_type_to (LineType or str): :class:`~.LineType` to convert to as enum or string
            equivalent.

    Return:
        Converted set of contour lines.

    When converting non-chunked line types (``LineType.Separate`` or ``LineType.SeparateCode``) to
    chunked ones (``LineType.ChunkCombinedCode``, ``LineType.ChunkCombinedOffset`` or
    ``LineType.ChunkCombinedNan``), all lines are placed in the first chunk. When converting in the
    other direction, all chunk information is discarded.

    .. versionadded:: 1.3.0
    """
    line_type_from = as_line_type(line_type_from)
    line_type_to = as_line_type(line_type_to)

    return [convert_lines(lines, line_type_from, line_type_to) for lines in multi_lines]

