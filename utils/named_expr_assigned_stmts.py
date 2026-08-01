
def named_expr_assigned_stmts(
    self: nodes.NamedExpr,
    node: node_classes.AssignedStmtsPossibleNode,
    context: InferenceContext | None = None,
    assign_path: list[int] | None = None,
) -> Any:
    """Infer names and other nodes from an assignment expression."""
    if self.target == node:
        yield from self.value.infer(context=context)
    else:
        raise InferenceError(
            "Cannot infer NamedExpr node {node!r}",
            node=self,
            assign_path=assign_path,
            context=context,
        )

