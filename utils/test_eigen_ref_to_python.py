
def test_eigen_ref_to_python():
    chols = [m.cholesky1, m.cholesky2, m.cholesky3, m.cholesky4]
    for i, chol in enumerate(chols, start=1):
        mymat = chol(np.array([[1.0, 2, 4], [2, 13, 23], [4, 23, 77]]))
        assert np.all(
            mymat == np.array([[1, 0, 0], [2, 3, 0], [4, 5, 6]])
        ), f"cholesky{i}"

