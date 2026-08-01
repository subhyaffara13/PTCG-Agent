
def test_rcode_ITE():
    expr = ITE(x < 1, y, z)
    p = rcode(expr)
    ref="ifelse(x < 1,y,z)"
    assert p == ref

