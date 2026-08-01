
def test_large_assignments():
    # When nnz grows bigger than int32 can hold, shift to int64 index arrays

    # This test requires *a lot* of memory!
    check_free_memory(65536)

    # parametrize puts lots of slow stuff into pytest's collection phase. So dont use it
    def check(A_info, index, rhs):
        if A_info is None:
            A = csr_array((d, d), dtype=np.int32)
        else:
            A = csr_array(A_info, shape=(d, d))

        # check that we start small
        assert A.indices.dtype == np.int32
        assert A.nnz < 2**31
        # do the assignment
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", warn_msg, sparse.SparseEfficiencyWarning)
            A[index[:, None], index] = rhs
        # check that we end large
        assert A.indices.dtype == np.int64
        assert A.nnz > 2**31

    N = 46340  # 46340**2 fits in int32, 46341**2 does not
    d = 47000  # d**2 > 2**31 with some extra room
    warn_msg = "Changing the sparsity structure"

    big_data = np.ones((N, N), dtype=np.float32)
    big_coords = tuple(co.astype(np.int32) for co in big_data.nonzero())
    big_data = big_data.reshape(-1)
    big_info = (big_data, big_coords)

    index_N = np.arange(N + 1, dtype=np.int32)
    index_300 = np.arange(N, N + 300, dtype=np.int32)

    rhs_300 = np.arange(300 * 300, dtype=np.float32).reshape((300, 300))
    rhs_300_sparse = csr_array(rhs_300)

    # 1: see gh-24915: From empty array, assign 1 to 46341x46341 region")
    check(None, index_N, 1)

    # 2: From 46340x46340 region filled, assign 1 to new 300x300 region")
    check(big_info, index_300, 1)

    # 3: From 46340x46340 region filled, assign np.array to new 300x300 region")
    check(big_info, index_300, rhs_300)

    # 4: From 46340x46340 region filled, assign sparse to new 300x300 region")
    check(big_info, index_300, rhs_300_sparse)

