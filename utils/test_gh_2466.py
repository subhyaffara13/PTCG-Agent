
def test_gh_2466():
    row = np.array([0, 0])
    col = np.array([0, 1])
    val = np.array([1, -1])
    A = scipy.sparse.coo_array((val, (row, col)), shape=(1, 2))
    b = np.asarray([4])
    lsqr(A, b)

