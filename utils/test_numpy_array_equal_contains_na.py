
def test_numpy_array_equal_contains_na():
    # https://github.com/pandas-dev/pandas/issues/31881
    a = np.array([True, False])
    b = np.array([True, pd.NA], dtype=object)

    msg = """numpy array are different

numpy array values are different \\(50.0 %\\)
\\[left\\]:  \\[True, False\\]
\\[right\\]: \\[True, <NA>\\]"""

    with pytest.raises(AssertionError, match=msg):
        tm.assert_numpy_array_equal(a, b)

