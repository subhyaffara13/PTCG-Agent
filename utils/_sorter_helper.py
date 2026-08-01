
def _sorter_helper(tb: TensorBox) -> tuple[str, sympy.Expr]:
    return tb.get_name(), tb.get_stride()[-1]

