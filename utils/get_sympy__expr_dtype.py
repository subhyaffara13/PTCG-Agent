
def get_sympy_Expr_dtype(val: sympy.Expr) -> torch.dtype:
    assert isinstance(val, sympy.Expr), (
        "only support sympy.Expr as input to get_sympy_Expr_dtype"
    )
    if val.is_integer:  # type: ignore[attr-defined]
        return torch.int64
    else:
        return torch.float64

