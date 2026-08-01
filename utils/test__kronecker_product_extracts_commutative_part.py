
def test_KroneckerProduct_extracts_commutative_part():
    assert kronecker_product(x * A, 2 * B) == x * \
        2 * KroneckerProduct(A, B)

