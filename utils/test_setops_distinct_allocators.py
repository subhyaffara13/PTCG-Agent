
def test_setops_distinct_allocators():
    vals = [f"{'v' * 16}{i:04d}" for i in range(90)]
    a = np.array(vals[:60], dtype="T")
    b = np.array(vals[30:], dtype="T")
    assert a.dtype is not b.dtype
    au = np.array(vals[:60], dtype="U20")
    bu = np.array(vals[30:], dtype="U20")

    assert_array_equal(np.isin(a, b), np.isin(au, bu))
    assert_array_equal(np.union1d(a, b), np.union1d(au, bu))
    assert_array_equal(np.intersect1d(a, b), np.intersect1d(au, bu))
    assert_array_equal(np.setdiff1d(a, b), np.setdiff1d(au, bu))
    assert_array_equal(np.setxor1d(a, b), np.setxor1d(au, bu))

    # StringDType has hasobject set, so isin always takes the
    # element-comparison loop and 'table' only supports integers
    assert_array_equal(
        np.isin(a, b, invert=True), np.isin(au, bu, invert=True)
    )
    assert_array_equal(np.isin(a, b[:4]), np.isin(au, bu[:4]))
    with pytest.raises(ValueError, match="table"):
        np.isin(a, b, kind="table")

    assert_array_equal(
        np.intersect1d(a, b, assume_unique=True),
        np.intersect1d(au, bu, assume_unique=True),
    )

    # duplicated entries exercise the sort-based unique path that
    # return_indices uses internally
    a_dup = np.array((vals[:40] * 2)[::-1], dtype="T")
    b_dup = np.array(vals[20:] + vals[60:], dtype="T")
    res = np.intersect1d(a_dup, b_dup, return_indices=True)
    expected = np.intersect1d(
        a_dup.astype("U20"), b_dup.astype("U20"), return_indices=True
    )
    for r, e in zip(res, expected):
        assert_array_equal(r, e)

