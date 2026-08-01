
def test_issue_6208():
    from sympy.functions.elementary.miscellaneous import root
    assert sqrt(33**(I*9/10)) == -33**(I*9/20)
    assert root((6*I)**(2*I), 3).as_base_exp()[1] == Rational(1, 3)  # != 2*I/3
    assert root((6*I)**(I/3), 3).as_base_exp()[1] == I/9
    assert sqrt(exp(3*I)) == exp(3*I/2)
    assert sqrt(-sqrt(3)*(1 + 2*I)) == sqrt(sqrt(3))*sqrt(-1 - 2*I)
    assert sqrt(exp(5*I)) == -exp(5*I/2)
    assert root(exp(5*I), 3).exp == Rational(1, 3)

