
def test_matrix_zeros_numpy():
    if not np:
        skip("numpy not installed.")

    num = matrix_zeros(4, 4, format='numpy')
    assert isinstance(num, numpy_ndarray)

