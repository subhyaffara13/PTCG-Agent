
def test_block_diag(shape):
    rng = np.random.default_rng(23409823)
    sp_x = random_array(shape, density=0.6, random_state=rng, dtype=int)
    den_x = sp_x.toarray()

    # converting n-d numpy array to an array of slices of 2-D matrices,
    # to pass as argument into scipy.linalg.block_diag
    num_slices = int(np.prod(den_x.shape[:-2]))
    reshaped_array = den_x.reshape((num_slices,) + den_x.shape[-2:])
    matrices = [reshaped_array[i, :, :] for i in range(num_slices)]
    exp = block_diag(*matrices)

    res = _block_diag(sp_x)

    assert_equal(res.toarray(), exp)

