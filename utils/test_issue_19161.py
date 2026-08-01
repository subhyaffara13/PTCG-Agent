
def test_issue_19161():
    polynomial = Poly('x**2').simplify()
    assert (polynomial-x**2).simplify() == 0

