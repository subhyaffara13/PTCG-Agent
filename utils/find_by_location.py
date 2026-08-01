
def find_by_location(
    tree: MypyFile, line: int, column: int, end_line: int, end_column: int
) -> Expression | None:
    """Find an expression matching given span, or None if not found."""
    if end_line < line:
        raise ValueError('"end_line" must not be before "line"')
    if end_line == line and end_column <= column:
        raise ValueError('"end_column" must be after "column"')
    visitor = SearchVisitor(line, column, end_line, end_column)
    tree.accept(visitor)
    return visitor.result

