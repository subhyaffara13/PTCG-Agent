
def test_tensor_product_conjugate():
    assert KroneckerProduct(I*A, B).conjugate() == \
        -I*KroneckerProduct(A.conjugate(), B.conjugate())
    assert KroneckerProduct(mat1, mat2).conjugate() == \
        kronecker_product(mat1.conjugate(), mat2.conjugate())

