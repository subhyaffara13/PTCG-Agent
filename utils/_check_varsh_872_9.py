
def _check_varsh_872_9(term_list):
    # Sum( CG(a,alpha,b,beta,c,gamma)*CG(a,alpha',b,beta',c,gamma), (gamma, -c, c), (c, abs(a-b), a+b))
    a, alpha, alphap, b, beta, betap, c, gamma, lt = map(Wild, (
        'a', 'alpha', 'alphap', 'b', 'beta', 'betap', 'c', 'gamma', 'lt'))
    # Case alpha==alphap, beta==betap

    # For numerical alpha,beta
    expr = lt*CG(a, alpha, b, beta, c, gamma)**2
    simp = S.One
    sign = lt/abs(lt)
    x = abs(a - b)
    y = abs(alpha + beta)
    build_expr = a + b + 1 - Piecewise((x, x > y), (0, Eq(x, y)), (y, y > x))
    index_expr = a + b - c
    term_list, other1 = _check_cg_simp(expr, simp, sign, lt, term_list, (a, alpha, b, beta, c, gamma, lt), (a, alpha, b, beta), build_expr, index_expr)

    # For symbolic alpha,beta
    x = abs(a - b)
    y = a + b
    build_expr = (y + 1 - x)*(x + y + 1)
    index_expr = (c - x)*(x + c) + c + gamma
    term_list, other2 = _check_cg_simp(expr, simp, sign, lt, term_list, (a, alpha, b, beta, c, gamma, lt), (a, alpha, b, beta), build_expr, index_expr)

    # Case alpha!=alphap or beta!=betap
    # Note: this only works with leading term of 1, pattern matching is unable to match when there is a Wild leading term
    # For numerical alpha,alphap,beta,betap
    expr = CG(a, alpha, b, beta, c, gamma)*CG(a, alphap, b, betap, c, gamma)
    simp = KroneckerDelta(alpha, alphap)*KroneckerDelta(beta, betap)
    sign = S.One
    x = abs(a - b)
    y = abs(alpha + beta)
    build_expr = a + b + 1 - Piecewise((x, x > y), (0, Eq(x, y)), (y, y > x))
    index_expr = a + b - c
    term_list, other3 = _check_cg_simp(expr, simp, sign, S.One, term_list, (a, alpha, alphap, b, beta, betap, c, gamma), (a, alpha, alphap, b, beta, betap), build_expr, index_expr)

    # For symbolic alpha,alphap,beta,betap
    x = abs(a - b)
    y = a + b
    build_expr = (y + 1 - x)*(x + y + 1)
    index_expr = (c - x)*(x + c) + c + gamma
    term_list, other4 = _check_cg_simp(expr, simp, sign, S.One, term_list, (a, alpha, alphap, b, beta, betap, c, gamma), (a, alpha, alphap, b, beta, betap), build_expr, index_expr)

    return term_list, other1 + other2 + other4

