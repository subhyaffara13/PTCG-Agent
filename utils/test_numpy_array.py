
def test_numpy_array():
    p = NumPyPrinter()
    assert p.doprint(Array([[1, 2], [3, 5]])) == 'numpy.array([[1, 2], [3, 5]])'
    assert p.doprint(Array([1, 2])) == 'numpy.array([1, 2])'
    assert p.doprint(Array([[[1, 2, 3]]])) == 'numpy.array([[[1, 2, 3]]])'
    assert p.doprint(Array([], (0,))) == 'numpy.zeros((0,))'
    assert p.doprint(Array([], (0, 0))) == 'numpy.zeros((0, 0))'
    assert p.doprint(Array([], (0, 1))) == 'numpy.zeros((0, 1))'
    assert p.doprint(Array([], (1, 0))) == 'numpy.zeros((1, 0))'
    assert p.doprint(Array([1], ())) == 'numpy.array(1)'


def test_numpy_array(arr):
    ser = Series(arr)
    result = ser.array
    expected = NumpyExtensionArray(arr)
    tm.assert_extension_array_equal(result, expected)


def test_numpy_array(input_dict, expected):
    result = np.array([Series(input_dict)])
    tm.assert_numpy_array_equal(result, expected)

