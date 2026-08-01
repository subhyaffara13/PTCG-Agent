
def test_KroneckerProduct_inverse():
    kp = kronecker_product(W, Z)
    assert kp.inverse() == kronecker_product(W.inverse(), Z.inverse())

