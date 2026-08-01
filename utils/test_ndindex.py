
def test_ndindex():
    x = list(ndindex(1, 2, 3))
    expected = [ix for ix, e in ndenumerate(np.zeros((1, 2, 3)))]
    assert_array_equal(x, expected)

    x = list(ndindex((1, 2, 3)))
    assert_array_equal(x, expected)

    # Test use of scalars and tuples
    x = list(ndindex((3,)))
    assert_array_equal(x, list(ndindex(3)))

    # Make sure size argument is optional
    x = list(ndindex())
    assert_equal(x, [()])

    x = list(ndindex(()))
    assert_equal(x, [()])

    # Make sure 0-sized ndindex works correctly
    x = list(ndindex(*[0]))
    assert_equal(x, [])

