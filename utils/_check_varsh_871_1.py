
def _check_varsh_871_1(term_list):
    # Sum( CG(a,alpha,b,0,a,alpha), (alpha, -a, a)) == KroneckerDelta(b,0)
    a, alpha, b, lt = map(Wild, ('a', 'alpha', 'b', 'lt'))
    expr = lt*CG(a, alpha, b, 0, a, alpha)
    simp = (2*a + 1)*KroneckerDelta(b, 0)
    sign = lt/abs(lt)
    build_expr = 2*a + 1
    index_expr = a + alpha
    return _check_cg_simp(expr, simp, sign, lt, term_list, (a, alpha, b, lt), (a, b), build_expr, index_expr)

