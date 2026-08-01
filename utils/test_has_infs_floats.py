
def test_has_infs_floats(request, arr, correct, astype, disable_bottleneck):
    val = request.getfixturevalue(arr)
    if astype is not None:
        val = val.astype(astype)
    while getattr(val, "ndim", True):
        res0 = nanops._has_infs(val)
        if correct:
            assert res0
        else:
            assert not res0

        if not hasattr(val, "ndim"):
            break

        # Reduce dimension for next step in the loop
        val = np.take(val, 0, axis=-1)

