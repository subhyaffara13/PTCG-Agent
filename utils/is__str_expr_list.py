
def is_StrExpr_list(seq: list[Expression]) -> TypeGuard[list[StrExpr]]:  # noqa: N802
    return all(isinstance(item, StrExpr) for item in seq)

