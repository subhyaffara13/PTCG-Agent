
def test_linsolve_underdetermined_AND_gauss_jordan_solve():
    #Test placement of free variables as per issue 19815
    A = Matrix([[1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                [0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1]])
    B  = Matrix([1, 2, 1, 1, 1, 1, 1, 2])
    sol, params = A.gauss_jordan_solve(B)
    w = {}
    for s in sol.atoms(Symbol):
        w[s.name] = s
    assert params == Matrix([[w['tau0']], [w['tau1']], [w['tau2']],
                             [w['tau3']], [w['tau4']], [w['tau5']]])
    assert sol == Matrix([[1 - 1*w['tau2']],
                          [w['tau2']],
                          [1 - 1*w['tau0'] + w['tau1']],
                          [w['tau0']],
                          [w['tau3'] + w['tau4']],
                          [-1*w['tau3'] - 1*w['tau4'] - 1*w['tau1']],
                          [1 - 1*w['tau2']],
                          [w['tau1']],
                          [w['tau2']],
                          [w['tau3']],
                          [w['tau4']],
                          [1 - 1*w['tau5']],
                          [w['tau5']],
                          [1]])

    from sympy.abc import j,f
    # https://github.com/sympy/sympy/issues/20046
    A = Matrix([
    [1,  1, 1,  1, 1,  1, 1,  1,  1],
    [0, -1, 0, -1, 0, -1, 0, -1, -j],
    [0,  0, 0,  0, 1,  1, 1,  1,  f]
    ])

    sol_1=Matrix(list(linsolve(A))[0])

    tau0, tau1, tau2, tau3, tau4 = symbols('tau:5')

    assert sol_1 == Matrix([[-f - j - tau0 + tau2 + tau4 + 1],
                          [j - tau1 - tau2 - tau4],
                          [tau0],
                          [tau1],
                          [f - tau2 - tau3 - tau4],
                          [tau2],
                          [tau3],
                          [tau4]])

    # https://github.com/sympy/sympy/issues/19815
    sol_2 = A[:, : -1 ] * sol_1 - A[:, -1 ]
    assert sol_2 == Matrix([[0], [0], [0]])

