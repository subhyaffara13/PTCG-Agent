
def test_N16():
    r, t = symbols('r t')
    solveset((r**2)*((cos(t) - 4)**2)*sin(t)**2 < 9, r, S.Reals)

