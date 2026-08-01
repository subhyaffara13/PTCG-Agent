
def test_really_large_scalar(large_val, signed, transform, errors):
    # see gh-24910
    kwargs = {"errors": errors} if errors is not None else {}
    val = -large_val if signed else large_val

    val = transform(val)

    expected = float(val) if errors == "coerce" else int(val)
    tm.assert_almost_equal(to_numeric(val, **kwargs), expected)

