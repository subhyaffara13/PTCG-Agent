
def test_KroneckerProduct_is_associative():
    assert kronecker_product(A, kronecker_product(
        B, C)) == kronecker_product(kronecker_product(A, B), C)
    assert kronecker_product(A, kronecker_product(
        B, C)) == KroneckerProduct(A, B, C)

