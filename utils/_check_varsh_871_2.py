
def _check_varsh_871_2(term_list):
    # Sum((-1)**(a-alpha)*CG(a,alpha,a,-alpha,c,0),(alpha,-a,a))
    a, alpha, c, lt = map(Wild, ('a', 'alpha', 'c', 'lt'))
    expr = lt*CG(a, alpha, a, -alpha, c, 0)
    simp = sqrt(2*a + 1)*KroneckerDelta(c, 0)
    sign = (-1)**(a - alpha)*lt/abs(lt)
    build_expr = 2*a + 1
    index_expr = a + alpha
    return _check_cg_simp(expr, simp, sign, lt, term_list, (a, alpha, c, lt), (a, c), build_expr, index_expr)

