
def test_as_strided():
    a = np.array([None])
    a_view = as_strided(a)
    expected = np.array([None])
    assert_array_equal(a_view, np.array([None]))

    a = np.array([1, 2, 3, 4])
    a_view = as_strided(a, shape=(2,), strides=(2 * a.itemsize,))
    expected = np.array([1, 3])
    assert_array_equal(a_view, expected)

    a = np.array([1, 2, 3, 4])
    a_view = as_strided(a, shape=(3, 4), strides=(0, 1 * a.itemsize))
    expected = np.array([[1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4]])
    assert_array_equal(a_view, expected)

    # Regression test for gh-5081
    dt = np.dtype([('num', 'i4'), ('obj', 'O')])
    a = np.empty((4,), dtype=dt)
    a['num'] = np.arange(1, 5)
    a_view = as_strided(a, shape=(3, 4), strides=(0, a.itemsize))
    expected_num = [[1, 2, 3, 4]] * 3
    expected_obj = [[None] * 4] * 3
    assert_equal(a_view.dtype, dt)
    assert_array_equal(expected_num, a_view['num'])
    assert_array_equal(expected_obj, a_view['obj'])

    # Make sure that void types without fields are kept unchanged
    a = np.empty((4,), dtype='V4')
    a_view = as_strided(a, shape=(3, 4), strides=(0, a.itemsize))
    assert_equal(a.dtype, a_view.dtype)

    # Make sure that the only type that could fail is properly handled
    dt = np.dtype({'names': [''], 'formats': ['V4']})
    a = np.empty((4,), dtype=dt)
    a_view = as_strided(a, shape=(3, 4), strides=(0, a.itemsize))
    assert_equal(a.dtype, a_view.dtype)

    # Custom dtypes should not be lost (gh-9161)
    r = [rational(i) for i in range(4)]
    a = np.array(r, dtype=rational)
    a_view = as_strided(a, shape=(3, 4), strides=(0, a.itemsize))
    assert_equal(a.dtype, a_view.dtype)
    assert_array_equal([r] * 3, a_view)

    # Also exercise the new-DType-API rational variant.
    r = [rational2(i) for i in range(4)]
    a = np.array(r, dtype=rational2)
    a_view = as_strided(a, shape=(3, 4), strides=(0, a.itemsize))
    assert_equal(a.dtype, a_view.dtype)
    assert_array_equal([r] * 3, a_view)

