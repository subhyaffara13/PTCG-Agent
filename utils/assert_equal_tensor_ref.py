import copy

def assert_equal_tensor_ref(mat, writeable=True, modified=None):
    assert mat.flags.writeable == writeable

    copy = np.array(tensor_ref)
    if modified is not None:
        copy[indices] = modified

    np.testing.assert_array_equal(mat, copy)

