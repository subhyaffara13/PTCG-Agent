
def test_rcode_Relational():
    assert rcode(Eq(x, y)) == "x == y"
    assert rcode(Ne(x, y)) == "x != y"
    assert rcode(Le(x, y)) == "x <= y"
    assert rcode(Lt(x, y)) == "x < y"
    assert rcode(Gt(x, y)) == "x > y"
    assert rcode(Ge(x, y)) == "x >= y"

