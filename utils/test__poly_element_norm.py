
def test_PolyElement_norm():
    k = QQ
    K = QQ.algebraic_field(sqrt(2))
    sqrt2 = K.unit
    _, X, Y = ring("x,y", k)
    _, x, y = ring("x,y", K)

    assert (x*y + sqrt2).norm() == X**2*Y**2 - 2

