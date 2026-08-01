
def test_CoordinateSymbol():
    x, y = R2_r.symbols
    r, theta = R2_p.symbols
    assert y.rewrite(R2_p) == r*sin(theta)

