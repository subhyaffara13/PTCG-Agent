
def dechunk_multi_lines(
    multi_lines: list[cpy.LineReturn],
    line_type: LineType | str,
) -> list[cpy.LineReturn]:
    """Return multiple sets of contour lines with all chunked data moved into the first chunks.

    Contour lines that are not chunked (``LineType.Separate`` and ``LineType.SeparateCode``) and
    those that are but only contain a single chunk are returned unmodified. Individual lines are
    unchanged, they are not geometrically combined.

    Args:
        multi_lines (nested sequence of arrays): Contour line data, such as returned by
            :meth:`.ContourGenerator.multi_lines`.
        line_type (LineType or str): Type of :meth:`~.ContourGenerator.lines` as enum or string
            equivalent.

    Return:
        Multiple sets of contour lines in a single chunk.

    .. versionadded:: 1.3.0
    """
    line_type = as_line_type(line_type)

    if line_type in (LineType.Separate, LineType.SeparateCode):
        # No-op if line_type is not chunked.
        return multi_lines

    return [dechunk_lines(lines, line_type) for lines in multi_lines]

