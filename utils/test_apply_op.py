
def test_apply_op():
    d = Density([Ket(0), 0.5], [Ket(1), 0.5])
    assert d.apply_op(XOp()) == Density([XOp()*Ket(0), 0.5],
                                        [XOp()*Ket(1), 0.5])

