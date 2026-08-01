
def test_issue_12984():
    if not numexpr:
        skip("numexpr not installed.")
    func_numexpr = lambdify((x,y,z), Piecewise((y, x >= 0), (z, x > -1)), numexpr)
    with ignore_warnings(RuntimeWarning):
        assert func_numexpr(1, 24, 42) == 24
        assert str(func_numexpr(-1, 24, 42)) == 'nan'

