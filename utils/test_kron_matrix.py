
def test_kron_matrix():
    # 2018-04-29: moved here from core.tests.test_shape_base.
    a = np.ones([2, 2])
    m = np.asmatrix(a)
    assert_equal(type(np.kron(a, a)), np.ndarray)
    assert_equal(type(np.kron(m, m)), np.matrix)
    assert_equal(type(np.kron(a, m)), np.matrix)
    assert_equal(type(np.kron(m, a)), np.matrix)

