
def node_starts_after(o: Node, line: int, column: int) -> bool:
    return o.line > line or o.line == line and o.column > column

