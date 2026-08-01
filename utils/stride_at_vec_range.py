
def stride_at_vec_range(
    index: sympy.Expr, var: sympy.Symbol, vec_length: int | None = None
):
    if vec_length:
        index = simplify_index_in_vec_range(index, var, vec_length)
    return stride_at(index, var)

