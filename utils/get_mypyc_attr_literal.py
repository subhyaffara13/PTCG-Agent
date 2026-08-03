from typing import Any

def get_mypyc_attr_literal(e: Expression) -> Any:
    """Convert an expression from a mypyc_attr decorator to a value.

    Supports a pretty limited range."""
    if isinstance(e, (StrExpr, IntExpr, FloatExpr)):
        return e.value
    elif isinstance(e, RefExpr) and e.fullname == "builtins.True":
        return True
    elif isinstance(e, RefExpr) and e.fullname == "builtins.False":
        return False
    elif isinstance(e, RefExpr) and e.fullname == "builtins.None":
        return None
    elif isinstance(e, IntExpr):
        return e.value
    return NotImplemented

