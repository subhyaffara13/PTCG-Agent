
def test_tensor_product_transpose():
    assert KroneckerProduct(I*A, B).transpose() == \
        I*KroneckerProduct(A.transpose(), B.transpose())
    assert KroneckerProduct(mat1, mat2).transpose() == \
        kronecker_product(mat1.transpose(), mat2.transpose())

