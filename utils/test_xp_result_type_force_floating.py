
def test_xp_result_type_force_floating(x, y, xp):
    # When `force_floating==True`, behavior of `xp_result_type`
    # should match that of `xp.result_type` with `1.0` appended to the set of
    # arguments (after converting lists to arrays of type `xp`).
    # If this raises a `TypeError`, which is the case when the result
    # type is not defined by the standard, the result type should be
    # the result type of any inexact (real or complex floating) arguments
    # and the default floating point type.
    if (is_torch(xp) and not(isinstance(x, str) or isinstance(y, str))
            and np.isscalar(x) and np.isscalar(y)):
        pytest.skip("See 3/27/2024 comment at  data-apis/array-api-compat#277")

    x = convert_type(x, xp)
    y = convert_type(y, xp)
    x_ref = xp.asarray(x) if isinstance(x, list) else x
    y_ref = xp.asarray(y) if isinstance(y, list) else y

    expected_error = None
    try:
        dtype_ref = xp.result_type(x_ref, y_ref, 1.0)
    except TypeError:
        args = []
        if is_inexact(x_ref, xp):
            args.append(x_ref)
        if is_inexact(y_ref, xp):
            args.append(y_ref)
        dtype_ref = xp.result_type(*args, xp.asarray(1.0))
    except Exception as e:
        expected_error = (type(e), str(e))

    if expected_error is not None:
        with pytest.raises(expected_error[0], match=expected_error[1]):
            xp_result_type(x, y, xp=xp)
        return

    dtype_res = xp_result_type(x, y, force_floating=True, xp=xp)
    assert dtype_res == dtype_ref

