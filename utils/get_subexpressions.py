
def get_subexpressions(node: Node) -> list[Expression]:
    visitor = SubexpressionFinder()
    node.accept(visitor)
    return visitor.expressions

