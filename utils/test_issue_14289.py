
def test_issue_14289():
    from sympy.polys.numberfields import to_number_field

    a = 1 - sqrt(2)
    b = to_number_field(a)
    assert b.as_expr() == a
    assert b.minpoly(a).expand() == 0

