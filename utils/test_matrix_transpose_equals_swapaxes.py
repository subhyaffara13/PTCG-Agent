
def test_matrix_transpose_equals_swapaxes(shape):
    num_of_axes = len(shape)
    vec = np.arange(shape[-1])
    arr = np.broadcast_to(vec, shape)
    tgt = np.swapaxes(arr, num_of_axes - 2, num_of_axes - 1)
    mT = arr.mT
    assert_array_equal(tgt, mT)


def test_matrix_transpose_equals_swapaxes(shape):
    num_of_axes = len(shape)
    vec = np.arange(shape[-1])
    arr = np.broadcast_to(vec, shape)

    rng = np.random.default_rng(42)
    mask = rng.choice([0, 1], size=shape)
    ma_arr = masked_array(data=arr, mask=mask)

    tgt = np.swapaxes(arr, num_of_axes - 2, num_of_axes - 1)
    assert_array_equal(tgt, ma_arr.mT)

