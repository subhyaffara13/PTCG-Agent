
def test_shape_axes_ndarray(func):
    # Test fftn and ifftn work with NumPy arrays for shape and axes arguments
    # Regression test for gh-13342
    a = np.random.rand(10, 10)

    expect = func(a, shape=(5, 5))
    actual = func(a, shape=np.array([5, 5]))
    assert_equal(expect, actual)

    expect = func(a, axes=(-1,))
    actual = func(a, axes=np.array([-1,]))
    assert_equal(expect, actual)

    expect = func(a, shape=(4, 7), axes=(1, 0))
    actual = func(a, shape=np.array([4, 7]), axes=np.array([1, 0]))
    assert_equal(expect, actual)

