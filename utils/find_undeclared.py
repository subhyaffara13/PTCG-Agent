
def find_undeclared(
    nodes: t.Iterable[nodes.Node], names: t.Iterable[str]
) -> t.Set[str]:
    """Check if the names passed are accessed undeclared.  The return value
    is a set of all the undeclared names from the sequence of names found.
    """
    visitor = UndeclaredNameVisitor(names)
    try:
        for node in nodes:
            visitor.visit(node)
    except VisitorExit:
        pass
    return visitor.undeclared

