
def test_pow_issue_1724():
    e = ((S.NegativeOne)**(S.One/3))
    assert e.conjugate().n() == e.n().conjugate()
    e = S('-2/3 - (-29/54 + sqrt(93)/18)**(1/3) - 1/(9*(-29/54 + sqrt(93)/18)**(1/3))')
    assert e.conjugate().n() == e.n().conjugate()
    e = 2**I
    assert e.conjugate().n() == e.n().conjugate()

