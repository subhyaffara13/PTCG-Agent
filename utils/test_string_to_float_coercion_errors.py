
def test_string_to_float_coercion_errors(dtype, res_dt, hug_val):
    # This test primarily tests setitem
    val = np.array(["3M"], dtype=dtype)[0]  # use the scalar

    with pytest.raises(ValueError):
        np.array(val, dtype=res_dt)

    val = np.array([hug_val], dtype=dtype)[0]  # use the scalar

    with np.errstate(all="warn"):
        with pytest.warns(RuntimeWarning):
            np.array(val, dtype=res_dt)

    with np.errstate(all="raise"):
        with pytest.raises(FloatingPointError):
            np.array(val, dtype=res_dt)

