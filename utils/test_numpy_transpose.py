
def test_numpy_transpose():
    if not numpy:
        skip("numpy not installed.")
    A = Matrix([[1, x], [0, 1]])
    f = lambdify((x), A.T, modules="numpy")
    numpy.testing.assert_array_equal(f(2), numpy.array([[1, 0], [2, 1]]))


def test_numpy_transpose(index_or_series_obj):
    msg = "the 'axes' parameter is not supported"
    obj = index_or_series_obj
    tm.assert_equal(np.transpose(obj), obj)

    with pytest.raises(ValueError, match=msg):
        np.transpose(obj, axes=1)

