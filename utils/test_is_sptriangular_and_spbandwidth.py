
def test_is_sptriangular_and_spbandwidth(nnz, fmt):
    with warnings.catch_warnings():
        warnings.simplefilter('ignore', SparseEfficiencyWarning)
        rng = np.random.default_rng(42)

        N = nnz // 2
        dens = 0.1
        A = random_array((N, N), density=dens, format="csr", rng=rng)
        A[1, 3] = A[3, 1] = 22  # ensure not upper or lower
        A = A.asformat(fmt)
        AU = triu(A, format=fmt)
        AL = tril(A, format=fmt)
        D = 0.1 * eye_array(N, format=fmt)

        assert is_sptriangular(A) == (False, False)
        assert is_sptriangular(AL) == (True, False)
        assert is_sptriangular(AU) == (False, True)
        assert is_sptriangular(D) == (True, True)

        assert spbandwidth(A) == scipy.linalg.bandwidth(A.toarray())
        assert spbandwidth(AU) == scipy.linalg.bandwidth(AU.toarray())
        assert spbandwidth(AL) == scipy.linalg.bandwidth(AL.toarray())
        assert spbandwidth(D) == scipy.linalg.bandwidth(D.toarray())

