
def test_froomroots():
    roots = [-2, 2]
    p = poly.Polynomial.fromroots(roots, symbol='z')
    assert_equal(p.symbol, 'z')

