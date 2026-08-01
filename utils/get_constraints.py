
def get_constraints(
    expr: _NameNodes, frame: nodes.LocalsDictNodeNG
) -> dict[nodes.If | nodes.IfExp, set[Constraint]]:
    """Returns the constraints for the given expression.

    The returned dictionary maps the node where the constraint was generated to the
    corresponding constraint(s).

    Constraints are computed statically by analysing the code surrounding expr.
    Currently this only supports constraints generated from if conditions.
    """
    current_node: nodes.NodeNG | None = expr
    constraints_mapping: dict[nodes.If | nodes.IfExp, set[Constraint]] = {}
    while current_node is not None and current_node is not frame:
        parent = current_node.parent
        if isinstance(parent, (nodes.If, nodes.IfExp)):
            branch, _ = parent.locate_child(current_node)
            constraints: set[Constraint] | None = None
            if branch == "body":
                constraints = set(_match_constraint(expr, parent.test))
            elif branch == "orelse":
                constraints = set(_match_constraint(expr, parent.test, invert=True))

            if constraints:
                constraints_mapping[parent] = constraints
        current_node = parent

    return constraints_mapping

