
def test_time_dep_bra():
    b = TimeDepBra(0, t)

    assert isinstance(b, TimeDepBra)
    assert isinstance(b, BraBase)
    assert isinstance(b, StateBase)
    assert isinstance(b, QExpr)

    assert b.label == (Integer(0),)
    assert b.args == (Integer(0), t)
    assert b.time == t

    assert b.dual_class() == TimeDepKet
    assert b.dual == TimeDepKet(0, t)

    k = TimeDepBra(x, 0.5)
    assert k.label == (x,)
    assert k.args == (x, sympify(0.5))

    assert TimeDepBra() == TimeDepBra("psi", "t")

