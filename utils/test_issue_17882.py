
def test_issue_17882():
    eq = -8*x**2/(9*(x**2 - 1)**(S(4)/3)) + 4/(3*(x**2 - 1)**(S(1)/3))
    assert unrad(eq) is None


def test_issue_17882():
    assert solveset(-8*x**2/(9*(x**2 - 1)**(S(4)/3)) + 4/(3*(x**2 - 1)**(S(1)/3)), x, S.Complexes) == \
        FiniteSet(sqrt(3), -sqrt(3))

