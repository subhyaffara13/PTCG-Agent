
def assign_assigned_stmts(
    self: nodes.AugAssign | nodes.Assign | nodes.AnnAssign | nodes.TypeAlias,
    node: node_classes.AssignedStmtsPossibleNode = None,
    context: InferenceContext | None = None,
    assign_path: list[int] | None = None,
) -> Any:
    if not assign_path:
        yield self.value
        return None
    yield from _resolve_assignment_parts(
        self.value.infer(context), assign_path, context
    )

    return {
        "node": self,
        "unknown": node,
        "assign_path": assign_path,
        "context": context,
    }

