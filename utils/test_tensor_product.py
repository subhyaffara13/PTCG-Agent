
def test_tensor_product():
    n = Symbol('n')
    hs1 = ComplexSpace(2)
    hs2 = ComplexSpace(n)

    h = hs1*hs2
    assert isinstance(h, TensorProductHilbertSpace)
    assert h.dimension == 2*n
    assert h.spaces == (hs1, hs2)

    h = hs2*hs2
    assert isinstance(h, TensorPowerHilbertSpace)
    assert h.base == hs2
    assert h.exp == 2
    assert h.dimension == n**2

    f = FockSpace()
    h = hs1*hs2*f
    assert h.dimension is oo


def test_tensor_product():
    # We are attempting to be rigourous and raise TypeError when a user tries
    # to combine bras, kets, and operators in a manner that doesn't make sense.
    # In particular, we are not trying to interpret regular ``*`` multiplication
    # as a tensor product.
    with raises(TypeError):
        k1*k1
    with raises(TypeError):
        b1*b1
    with raises(TypeError):
        k1*TensorProduct(k2, k3)
    with raises(TypeError):
        b1*TensorProduct(b2, b3)
    with raises(TypeError):
        TensorProduct(k2, k3)*k1
    with raises(TypeError):
        TensorProduct(b2, b3)*b1

    assert TensorProduct(A, B, C)*TensorProduct(k1, k2, k3) == \
        TensorProduct(A*k1, B*k2, C*k3)
    assert TensorProduct(b1, b2, b3)*TensorProduct(A, B, C) == \
        TensorProduct(b1*A, b2*B, b3*C)
    assert TensorProduct(b1, b2, b3)*TensorProduct(k1, k2, k3) == \
        InnerProduct(b1, k1)*InnerProduct(b2, k2)*InnerProduct(b3, k3)
    assert TensorProduct(b1, b2, b3)*TensorProduct(A, B, C)*TensorProduct(k1, k2, k3) == \
        TensorProduct(b1*A*k1, b2*B*k2, b3*C*k3)

