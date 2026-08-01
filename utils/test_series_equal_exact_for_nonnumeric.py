
def test_series_equal_exact_for_nonnumeric():
    # https://github.com/pandas-dev/pandas/issues/35446
    s1 = Series(["a", "b"])
    s2 = Series(["a", "b"])
    s3 = Series(["b", "a"])

    tm.assert_series_equal(s1, s2, check_exact=True)
    tm.assert_series_equal(s2, s1, check_exact=True)

    msg = """Series are different

Series values are different \\(100\\.0 %\\)
\\[index\\]: \\[0, 1\\]
\\[left\\]:  \\[a, b\\]
\\[right\\]: \\[b, a\\]"""
    with pytest.raises(AssertionError, match=msg):
        tm.assert_series_equal(s1, s3, check_exact=True)

    msg = """Series are different

Series values are different \\(100\\.0 %\\)
\\[index\\]: \\[0, 1\\]
\\[left\\]:  \\[b, a\\]
\\[right\\]: \\[a, b\\]"""
    with pytest.raises(AssertionError, match=msg):
        tm.assert_series_equal(s3, s1, check_exact=True)

