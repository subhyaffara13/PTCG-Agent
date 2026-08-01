
def test_qexpr_free_symbols():
    q1 = QExpr(x, y)
    assert q1.free_symbols == {x, y}

