
def test_issue_22561():
    a = AlgebraicNumber(sqrt(2) + sqrt(3), [S(1) / 2, 0, S(-9) / 2, 0], gen=x)
    assert a.as_expr() == sqrt(2)
    assert minimal_polynomial(a, x) == x**2 - 2
    assert minimal_polynomial(a**3, x) == x**2 - 8


def test_issue_22561():
    a = to_number_field(sqrt(2), sqrt(2) + sqrt(3))
    b = to_number_field(sqrt(2), sqrt(2) + sqrt(5))
    assert field_isomorphism(a, b) == [1, 0]

