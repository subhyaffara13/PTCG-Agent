
def test_nd_add_sparse_with_inconsistent_shapes(a_shape, b_shape):
    rng = np.random.default_rng(23409823)

    arr_a = random_array((a_shape), density=0.6, rng=rng, dtype=int)
    arr_b = random_array((b_shape), density=0.6, rng=rng, dtype=int)
    with pytest.raises(ValueError, match="inconsistent shapes"):
        arr_a + arr_b

