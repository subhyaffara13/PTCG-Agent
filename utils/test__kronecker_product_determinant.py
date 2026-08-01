
def test_KroneckerProduct_determinant():
    kp = kronecker_product(W, Z)
    assert det(kp) == det(W)**n * det(Z)**m

