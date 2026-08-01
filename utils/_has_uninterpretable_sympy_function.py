
def _has_uninterpretable_sympy_function(expr: sympy.Basic) -> bool:
    """
    Add functions that our sympy interpreter can't reify into FX nodes
    """
    return expr.has(
        torch.utils._sympy.functions.ToFloat,
        torch.utils._sympy.functions.TruncToInt,
        torch.utils._sympy.functions.CeilToInt,
    )

