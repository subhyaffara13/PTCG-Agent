
def test_qexpr():
    q = QExpr('q')
    assert str(q) == 'q'
    assert pretty(q) == 'q'
    assert upretty(q) == 'q'
    assert latex(q) == r'q'
    sT(q, "QExpr(Symbol('q'))")

