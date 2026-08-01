
def test_regression_allowlist_methods(op, skipna, sort):
    # GH6944
    # GH 17537
    # explicitly test the allowlist methods
    frame = DataFrame([0])

    grouped = frame.groupby(level=0, sort=sort)

    if op in ["skew", "kurt", "sum", "mean"]:
        # skew, kurt, sum, mean have skipna
        result = getattr(grouped, op)(skipna=skipna)
        expected = frame.groupby(level=0).apply(lambda h: getattr(h, op)(skipna=skipna))
        if sort:
            expected = expected.sort_index()
        tm.assert_frame_equal(result, expected)
    else:
        result = getattr(grouped, op)()
        expected = frame.groupby(level=0).apply(lambda h: getattr(h, op)())
        if sort:
            expected = expected.sort_index()
        tm.assert_frame_equal(result, expected)

