
def _iter_syntax_lines(
    start: SyntaxPosition, end: SyntaxPosition
) -> Iterable[Tuple[int, int, int]]:
    """Yield start and end positions per line.

    Args:
        start: Start position.
        end: End position.

    Returns:
        Iterable of (LINE, COLUMN1, COLUMN2).
    """

    line1, column1 = start
    line2, column2 = end

    if line1 == line2:
        yield line1, column1, column2
    else:
        for first, last, line_no in loop_first_last(range(line1, line2 + 1)):
            if first:
                yield line_no, column1, -1
            elif last:
                yield line_no, 0, column2
            else:
                yield line_no, 0, -1


def _iter_syntax_lines(
    start: SyntaxPosition, end: SyntaxPosition
) -> Iterable[Tuple[int, int, int]]:
    """Yield start and end positions per line.

    Args:
        start: Start position.
        end: End position.

    Returns:
        Iterable of (LINE, COLUMN1, COLUMN2).
    """

    line1, column1 = start
    line2, column2 = end

    if line1 == line2:
        yield line1, column1, column2
    else:
        for first, last, line_no in loop_first_last(range(line1, line2 + 1)):
            if first:
                yield line_no, column1, -1
            elif last:
                yield line_no, 0, column2
            else:
                yield line_no, 0, -1

