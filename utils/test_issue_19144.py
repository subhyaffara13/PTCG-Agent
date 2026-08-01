
def test_issue_19144():
    # test case 1
    expr1 = [x + y - 1, y**2 + 1]
    eq1 = [Eq(i, 0) for i in expr1]
    soln1 = {(1 - I, I), (1 + I, -I)}
    soln_expr1 = nonlinsolve(expr1, [x, y])
    soln_eq1 = nonlinsolve(eq1, [x, y])
    assert soln_eq1 == soln_expr1 == soln1
    # test case 2 - with denoms
    expr2 = [x/y - 1, y**2 + 1]
    eq2 = [Eq(i, 0) for i in expr2]
    soln2 = {(-I, -I), (I, I)}
    soln_expr2 = nonlinsolve(expr2, [x, y])
    soln_eq2 = nonlinsolve(eq2, [x, y])
    assert soln_eq2 == soln_expr2 == soln2
    # denominators that cancel in expression
    assert nonlinsolve([Eq(x + 1/x, 1/x)], [x]) == FiniteSet((S.EmptySet,))

