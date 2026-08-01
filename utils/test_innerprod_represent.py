
def test_innerprod_represent():
    assert rep_innerproduct(x_ket) == InnerProduct(XBra("x_1"), x_ket).doit()
    assert rep_innerproduct(x_bra) == InnerProduct(x_bra, XKet("x_1")).doit()
    raises(TypeError, lambda: rep_innerproduct(x_op))

