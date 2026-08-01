
def find_all_by_location(tree: MypyFile, line: int, column: int) -> list[Expression]:
    """Find all expressions enclosing given position starting from innermost."""
    visitor = SearchAllVisitor(line, column)
    tree.accept(visitor)
    return list(reversed(visitor.result))

