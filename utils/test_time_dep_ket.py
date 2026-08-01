
def test_time_dep_ket():
    k = TimeDepKet(0, t)

    assert isinstance(k, TimeDepKet)
    assert isinstance(k, KetBase)
    assert isinstance(k, StateBase)
    assert isinstance(k, QExpr)

    assert k.label == (Integer(0),)
    assert k.args == (Integer(0), t)
    assert k.time == t

    assert k.dual_class() == TimeDepBra
    assert k.dual == TimeDepBra(0, t)

    assert k.subs(t, 2) == TimeDepKet(0, 2)

    k = TimeDepKet(x, 0.5)
    assert k.label == (x,)
    assert k.args == (x, sympify(0.5))

    k = CustomTimeDepKet()
    assert k.label == (Symbol("test"),)
    assert k.time == Symbol("t")
    assert k == CustomTimeDepKet("test", "t")

    k = CustomTimeDepKetMultipleLabels()
    assert k.label == (Symbol("r"), Symbol("theta"), Symbol("phi"))
    assert k.time == Symbol("t")
    assert k == CustomTimeDepKetMultipleLabels("r", "theta", "phi", "t")

    assert TimeDepKet() == TimeDepKet("psi", "t")

