
def is_sys_attr(expr: Expression, name: str) -> bool:
    # TODO: This currently doesn't work with code like this:
    # - import sys as _sys
    # - from sys import version_info
    if isinstance(expr, MemberExpr) and expr.name == name:
        if isinstance(expr.expr, NameExpr) and expr.expr.name == "sys":
            # TODO: Guard against a local named sys, etc.
            # (Though later passes will still do most checking.)
            return True
    return False

