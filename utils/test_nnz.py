
def test_nnz():
    arr1d = coo_array([1, 0, 3])
    assert arr1d.shape == (3,)
    assert arr1d.nnz == 2

    arr2d = coo_array([[1, 2, 0], [0, 0, 3]])
    assert arr2d.shape == (2, 3)
    assert arr2d.nnz == 3

