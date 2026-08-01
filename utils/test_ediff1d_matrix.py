
def test_ediff1d_matrix():
    # 2018-04-29: moved here from core.tests.test_arraysetops.
    assert isinstance(np.ediff1d(np.matrix(1)), np.matrix)
    assert isinstance(np.ediff1d(np.matrix(1), to_begin=1), np.matrix)

