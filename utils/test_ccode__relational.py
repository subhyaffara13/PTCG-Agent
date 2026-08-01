
def test_ccode_Relational():
    assert ccode(Eq(x, y)) == "x == y"
    assert ccode(Ne(x, y)) == "x != y"
    assert ccode(Le(x, y)) == "x <= y"
    assert ccode(Lt(x, y)) == "x < y"
    assert ccode(Gt(x, y)) == "x > y"
    assert ccode(Ge(x, y)) == "x >= y"

