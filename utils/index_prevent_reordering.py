
def index_prevent_reordering(
    index: Sequence[sympy.Expr],
    index_vars: Sequence[sympy.Expr],
    sizes: Sequence[sympy.Expr],
) -> list[sympy.Expr]:
    from ..ir import FlexibleLayout

    # added contiguous index prevents reordering
    return [*index, sympy_dot(index_vars, FlexibleLayout.contiguous_strides(sizes))]

