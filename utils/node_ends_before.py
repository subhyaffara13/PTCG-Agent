
def node_ends_before(o: Node, line: int, column: int) -> bool:
    # Unfortunately, end positions for some statements are a mess,
    # e.g. overloaded functions, so we return False when we don't know.
    if o.end_line is not None and o.end_column is not None:
        if o.end_line < line or o.end_line == line and o.end_column < column:
            return True
    return False

