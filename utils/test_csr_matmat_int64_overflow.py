
def test_csr_matmat_int64_overflow():
    n = 3037000500
    assert n**2 > np.iinfo(np.int64).max

    # the test would take crazy amounts of memory
    check_free_memory(n * (8*2 + 1) * 3 / 1e6)

    # int64 overflow
    data = np.ones((n,), dtype=np.int8)
    indptr = np.arange(n+1, dtype=np.int64)
    indices = np.zeros(n, dtype=np.int64)
    a = csr_matrix((data, indices, indptr))
    b = a.T

    assert_raises(RuntimeError, a.dot, b)

