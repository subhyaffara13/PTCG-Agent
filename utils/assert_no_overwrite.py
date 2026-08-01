
def assert_no_overwrite(call, shapes, dtypes=None):
    """
    Test that a call does not overwrite its input arguments
    """

    if dtypes is None:
        dtypes = [np.float32, np.float64, np.complex64, np.complex128]

    for dtype in dtypes:
        for order in ["C", "F"]:
            for faker in [_id, _FakeMatrix, _FakeMatrix2]:
                orig_inputs = [_get_array(s, dtype) for s in shapes]
                inputs = [faker(x.copy(order)) for x in orig_inputs]
                call(*inputs)
                msg = f"call modified inputs [{dtype!r}, {faker!r}]"
                for a, b in zip(inputs, orig_inputs):
                    np.testing.assert_equal(a, b, err_msg=msg)

