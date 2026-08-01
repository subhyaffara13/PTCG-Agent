
def test_build_order():
    R = QQ.old_poly_ring(x, y, order=(("lex", x), ("ilex", y)))
    assert R.order((1, 5)) == ((1,), (-5,))

