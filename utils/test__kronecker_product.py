
def test_KroneckerProduct():
    assert isinstance(KroneckerProduct(A, B), KroneckerProduct)
    assert KroneckerProduct(A, B).subs(A, C) == KroneckerProduct(C, B)
    assert KroneckerProduct(A, C).shape == (n*m, m*k)
    assert (KroneckerProduct(A, C) + KroneckerProduct(-A, C)).is_ZeroMatrix
    assert (KroneckerProduct(W, Z) * KroneckerProduct(W.I, Z.I)).is_Identity

