
def apply_function_specialization(
    builder: IRBuilder, expr: CallExpr, callee: RefExpr
) -> Value | None:
    """Invoke the Specializer callback for a function if one has been registered"""
    return _apply_specialization(builder, expr, callee, get_call_target_fullname(callee))

