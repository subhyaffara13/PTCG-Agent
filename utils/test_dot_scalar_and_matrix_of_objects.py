
def test_dot_scalar_and_matrix_of_objects():
    # Ticket #2469
    # 2018-04-29: moved here from core.tests.test_multiarray
    arr = np.matrix([1, 2], dtype=object)
    desired = np.matrix([[3, 6]], dtype=object)
    assert_equal(np.dot(arr, 3), desired)
    assert_equal(np.dot(3, arr), desired)

