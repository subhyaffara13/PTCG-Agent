
def test_object_scalar_multiply():
    # Tickets #2469 and #4482
    # 2018-04-29: moved here from core.tests.test_ufunc
    arr = np.matrix([1, 2], dtype=object)
    desired = np.matrix([[3, 6]], dtype=object)
    assert_equal(np.multiply(arr, 3), desired)
    assert_equal(np.multiply(3, arr), desired)

