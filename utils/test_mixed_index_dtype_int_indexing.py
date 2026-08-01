
def test_mixed_index_dtype_int_indexing(cls):
    # https://github.com/scipy/scipy/issues/20182
    rng = np.random.default_rng(0)
    base_mtx = cls(sparse.random(50, 50, random_state=rng, density=0.1))
    indptr_64bit = base_mtx.copy()
    indices_64bit = base_mtx.copy()
    indptr_64bit.indptr = base_mtx.indptr.astype(np.int64)
    indices_64bit.indices = base_mtx.indices.astype(np.int64)

    for mtx in [base_mtx, indptr_64bit, indices_64bit]:
        np.testing.assert_array_equal(
            mtx[[1,2], :].toarray(),
            base_mtx[[1, 2], :].toarray()
        )
        np.testing.assert_array_equal(
            mtx[:, [1, 2]].toarray(),
            base_mtx[:, [1, 2]].toarray()
        )

