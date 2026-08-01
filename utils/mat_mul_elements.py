
def MatMul_elements(matrix_predicate, scalar_predicate, expr, assumptions):
    d = sift(expr.args, lambda x: isinstance(x, MatrixExpr))
    factors, matrices = d[False], d[True]
    return fuzzy_and([
        test_closed_group(Basic(*factors), assumptions, scalar_predicate),
        test_closed_group(Basic(*matrices), assumptions, matrix_predicate)])

