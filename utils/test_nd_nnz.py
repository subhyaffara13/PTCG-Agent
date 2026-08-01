
def test_nd_nnz(shape):
    rng = np.random.default_rng(23409823)

    arr = random_array(shape, density=0.6, rng=rng, dtype=int)
    assert arr.nnz == np.count_nonzero(arr.toarray())

