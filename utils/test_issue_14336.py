
def test_issue_14336():
    #https://github.com/sympy/sympy/issues/14336
    U = S.Complexes
    x = Symbol("x")
    U -= U.intersect(Ne(x, 1).as_set())
    U -= U.intersect(S.true.as_set())

