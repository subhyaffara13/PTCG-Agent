
def _looks_like_dataclass_field_call(
    node: nodes.Call, check_scope: bool = True
) -> bool:
    """Return True if node is calling dataclasses field or Field
    from an AnnAssign statement directly in the body of a ClassDef.

    If check_scope is False, skips checking the statement and body.
    """
    if check_scope:
        stmt = node.statement()
        scope = stmt.scope()
        if not (
            isinstance(stmt, nodes.AnnAssign)
            and stmt.value is not None
            and isinstance(scope, nodes.ClassDef)
            and is_decorated_with_dataclass(scope)
        ):
            return False

    try:
        inferred = next(node.func.infer())
    except (InferenceError, StopIteration):
        return False

    if not isinstance(inferred, nodes.FunctionDef):
        return False

    return inferred.name == FIELD_NAME and inferred.root().name in DATACLASS_MODULES

