
def test_really_large_in_arr(large_val, signed, transform, multiple_elts, errors):
    # see gh-24910
    kwargs = {"errors": errors} if errors is not None else {}
    val = -large_val if signed else large_val
    val = transform(val)

    extra_elt = "string"
    arr = [val] + multiple_elts * [extra_elt]

    coercing = errors == "coerce"

    if errors in (None, "raise") and multiple_elts:
        msg = 'Unable to parse string "string" at position 1'

        with pytest.raises(ValueError, match=msg):
            to_numeric(arr, **kwargs)
    else:
        result = to_numeric(arr, **kwargs)

        exp_val = float(val) if (coercing) else int(val)
        expected = [exp_val]

        if multiple_elts:
            if coercing:
                expected.append(np.nan)
                exp_dtype = float
            else:
                expected.append(extra_elt)
                exp_dtype = object
        else:
            exp_dtype = float if isinstance(exp_val, float) else object

        tm.assert_almost_equal(result, np.array(expected, dtype=exp_dtype))

