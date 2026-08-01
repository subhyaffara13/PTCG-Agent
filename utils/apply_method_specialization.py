
def apply_method_specialization(
    builder: IRBuilder, expr: CallExpr, callee: MemberExpr, typ: RType | None = None
) -> Value | None:
    """Invoke the Specializer callback for a method if one has been registered"""
    name = callee.fullname if typ is None else callee.name
    return _apply_specialization(builder, expr, callee, name, typ)

