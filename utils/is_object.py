
def is_object(checker, instance):
    return isinstance(instance, dict)


def is_object(t: ProperType) -> bool:
    return isinstance(t, Instance) and t.type.fullname == "builtins.object"


def is_object(callee: RefExpr) -> bool:
    """Returns True for object.<name> calls."""
    return (
        isinstance(callee, MemberExpr)
        and isinstance(callee.expr, NameExpr)
        and callee.expr.fullname == "builtins.object"
    )

