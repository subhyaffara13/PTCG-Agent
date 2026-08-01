
def test_np_matmul_1D(box, using_python_scalars):
    result = np.matmul(box([1, 2]), box([2, 3]))
    assert result == 8
    if using_python_scalars:
        assert type(result) == int, type(result)
    else:
        assert type(result) == np.int64, type(result)

