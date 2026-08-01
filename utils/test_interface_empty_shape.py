
def test_interface_empty_shape():
    class ArrayLike:
        array = np.array(1)
        __array_interface__ = array.__array_interface__
    assert_equal(np.array(ArrayLike()), 1)

