
def test_KroneckerProduct_isnt_commutative():
    assert KroneckerProduct(A, B) != KroneckerProduct(B, A)
    assert KroneckerProduct(A, B).is_commutative is False

