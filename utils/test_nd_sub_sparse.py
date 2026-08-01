
def test_nd_sub_sparse(shape):
    rng = np.random.default_rng(23409823)

    sp_x = random_array(shape, density=0.6, rng=rng, dtype=int)
    sp_y = random_array(shape, density=0.6, rng=rng, dtype=int)
    den_x, den_y = sp_x.toarray(), sp_y.toarray()

    dense_sum = den_x - den_y
    sparse_sum = sp_x - sp_y
    assert_equal(dense_sum, sparse_sum.toarray())

