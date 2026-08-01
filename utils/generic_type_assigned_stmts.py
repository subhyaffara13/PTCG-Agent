
def generic_type_assigned_stmts(
    self: nodes.TypeVar | nodes.TypeVarTuple | nodes.ParamSpec,
    node: nodes.AssignName,
    context: InferenceContext | None = None,
    assign_path: None = None,
) -> Generator[nodes.NodeNG]:
    """Hack. Return any Node so inference doesn't fail
    when evaluating __class_getitem__. Revert if it's causing issues.
    """
    yield nodes.Const(None)

