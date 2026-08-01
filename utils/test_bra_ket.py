
def test_bra_ket():
    assert k.kind == KetKind
    assert b.kind == BraKind
    assert (b*k).kind == NumberKind # inner product
    assert (x*k).kind == KetKind
    assert (x*b).kind == BraKind


def test_bra_ket():
    assert b1*k1 == InnerProduct(b1, k1)
    assert k1*b1 == OuterProduct(k1, b1)
    # Test priority of inner product
    assert OuterProduct(k1, b1)*k2 == InnerProduct(b1, k2)*k1
    assert b1*OuterProduct(k1, b2) == InnerProduct(b1, k1)*b2

