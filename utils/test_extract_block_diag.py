
def test_extract_block_diag(shape):
    rng = np.random.default_rng(23409823)
    sp_x = random_array(shape, density=0.6, random_state=rng, dtype=int)
    res = _extract_block_diag(_block_diag(sp_x), shape)

    assert_equal(res.toarray(), sp_x.toarray())

