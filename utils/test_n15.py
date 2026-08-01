
def test_N15():
    r, t = symbols('r t')
    # raises NotImplementedError: only univariate inequalities are supported
    solveset(abs(2*r*(cos(t) - 1) + 1) <= 1, r, S.Reals)

