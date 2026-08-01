
def is_trait_decorator(d: Expression) -> bool:
    return isinstance(d, RefExpr) and d.fullname == "mypy_extensions.trait"

