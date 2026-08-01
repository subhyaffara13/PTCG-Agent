
def test_KroneckerProduct_trace():
    kp = kronecker_product(W, Z)
    assert trace(kp) == trace(W)*trace(Z)

