
def test_constant_renumber_order_issue_5308():
    from sympy.utilities.iterables import variations

    assert constant_renumber(C1*x + C2*y) == \
        constant_renumber(C1*y + C2*x) == \
        C1*x + C2*y
    e = C1*(C2 + x)*(C3 + y)
    for a, b, c in variations([C1, C2, C3], 3):
        assert constant_renumber(a*(b + x)*(c + y)) == e

