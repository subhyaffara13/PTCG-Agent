
def assign_annassigned_stmts(
    self: nodes.AnnAssign,
    node: node_classes.AssignedStmtsPossibleNode = None,
    context: InferenceContext | None = None,
    assign_path: list[int] | None = None,
) -> Any:
    for inferred in assign_assigned_stmts(self, node, context, assign_path):
        if inferred is None:
            yield util.Uninferable
        else:
            yield inferred

