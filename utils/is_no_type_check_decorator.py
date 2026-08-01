
def is_no_type_check_decorator(expr: ast3.expr) -> bool:
    if isinstance(expr, Name):
        return expr.id == "no_type_check"
    elif isinstance(expr, Attribute):
        if isinstance(expr.value, Name):
            return expr.value.id == "typing" and expr.attr == "no_type_check"
    return False

