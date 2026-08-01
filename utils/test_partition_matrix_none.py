
def test_partition_matrix_none():
    # gh-4301
    # 2018-04-29: moved here from core.tests.test_multiarray
    a = np.matrix([[2, 1, 0]])
    actual = np.partition(a, 1, axis=None)
    expected = np.matrix([[0, 1, 2]])
    assert_equal(actual, expected)
    assert_(type(expected) is np.matrix)

