
def test_nd_matmul_sparse_with_inconsistent_arrays():
    rng = np.random.default_rng(23409823)

    sp_x = random_array((4,5,7,6,3), density=0.6, random_state=rng, dtype=int)
    sp_y = random_array((1,5,3,2,5), density=0.6, random_state=rng, dtype=int)
    with pytest.raises(ValueError, match="matmul: dimension mismatch with signature"):
        sp_x @ sp_y
    with pytest.raises(ValueError, match="matmul: dimension mismatch with signature"):
        sp_x @ (sp_y.toarray())

    sp_z = random_array((1,5,3,2), density=0.6, random_state=rng, dtype=int)
    with pytest.raises(ValueError, match="Batch dimensions are not broadcastable"):
        sp_x @ sp_z
    with pytest.raises(ValueError, match="Batch dimensions are not broadcastable"):
        sp_x @ (sp_z.toarray())

