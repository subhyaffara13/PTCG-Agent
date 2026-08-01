
def test_KroneckerProduct_identity():
    assert KroneckerProduct(Identity(m), Identity(n)) == Identity(m*n)
    assert KroneckerProduct(eye(2), eye(3)) == eye(6)

