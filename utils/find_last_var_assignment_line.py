
def find_last_var_assignment_line(n: Node, v: Var) -> int:
    """Find the highest line number of a potential assignment to variable within node.

    This supports local and global variables.

    Return -1 if no assignment was found.
    """
    visitor = VarAssignVisitor(v)
    n.accept(visitor)
    return visitor.last_line

