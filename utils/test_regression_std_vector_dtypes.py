
def test_regression_std_vector_dtypes():
    # Regression test for gh-3780, checking the std::vector typemaps
    # in sparsetools.cxx are complete.
    for dtype in supported_dtypes:
        ad = np.array([[1, 2], [3, 4]]).astype(dtype)
        a = csr_matrix(ad, dtype=dtype)

        # getcol is one function using std::vector typemaps, and should not fail
        assert_equal(a.getcol(0).toarray(), ad[:, :1])

