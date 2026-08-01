
def test_drop_metadata_identity_and_copy(dtype):
    # If there is no metadata, the identity is preserved:
    assert _utils_impl.drop_metadata(dtype) is dtype

    # If there is any, it is dropped (subforms are checked above)
    dtype = np.dtype(dtype, metadata={1: 2})
    assert _utils_impl.drop_metadata(dtype).metadata is None

