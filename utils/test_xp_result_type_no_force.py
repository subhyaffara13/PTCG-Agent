import re

def test_xp_result_type_no_force(x, y, xp):
    # When force_floating==False (default), behavior of `xp_result_type`
    # should match that of `xp.result_type` on the same arguments after
    # converting lists to arrays of type `xp`.
    x = convert_type(x, xp)
    y = convert_type(y, xp)
    x_ref = xp.asarray(x) if isinstance(x, list) else x
    y_ref = xp.asarray(y) if isinstance(y, list) else y

    try:
        dtype_ref = xp.result_type(x_ref, y_ref)
        expected_error = None
    except Exception as e:
        expected_error = (type(e), str(e))

    if expected_error is not None:
        with pytest.raises(expected_error[0], match=re.escape(expected_error[1])):
            xp_result_type(x, y, xp=xp)
        return

    dtype_res = xp_result_type(x, y, xp=xp)
    assert dtype_res == dtype_ref

