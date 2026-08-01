
def test_KroneckerProduct_combine_add():
    kp1 = kronecker_product(A, B)
    kp2 = kronecker_product(C, W)
    assert combine_kronecker(kp1*kp2) == kronecker_product(A*C, B*W)

