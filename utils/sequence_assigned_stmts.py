
def sequence_assigned_stmts(
    self: nodes.Tuple | nodes.List,
    node: node_classes.AssignedStmtsPossibleNode = None,
    context: InferenceContext | None = None,
    assign_path: list[int] | None = None,
) -> Any:
    if assign_path is None:
        assign_path = []
    try:
        index = self.elts.index(node)  # type: ignore[arg-type]
    except ValueError as exc:
        raise InferenceError(
            "Tried to retrieve a node {node!r} which does not exist",
            node=self,
            assign_path=assign_path,
            context=context,
        ) from exc

    assign_path.insert(0, index)
    return self.parent.assigned_stmts(
        node=self, context=context, assign_path=assign_path
    )

