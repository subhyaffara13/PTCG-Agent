
def test_KroneckerProduct_is_bilinear():
    assert kronecker_product(x*A, B) == x*kronecker_product(A, B)
    assert kronecker_product(A, x*B) == x*kronecker_product(A, B)

