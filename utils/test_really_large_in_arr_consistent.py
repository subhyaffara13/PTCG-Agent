
def test_really_large_in_arr_consistent(large_val, signed, multiple_elts, errors):
    # see gh-24910
    #
    # Even if we discover that we have to hold float, does not mean
    # we should be lenient on subsequent elements that fail to be integer.
    kwargs = {"errors": errors} if errors is not None else {}
    arr = [str(-large_val if signed else large_val)]

    if multiple_elts:
        arr.insert(0, large_val)

    result = to_numeric(arr, **kwargs)
    expected = [float(i) if errors == "coerce" else int(i) for i in arr]
    exp_dtype = float if errors == "coerce" else object

    tm.assert_almost_equal(result, np.array(expected, dtype=exp_dtype))

