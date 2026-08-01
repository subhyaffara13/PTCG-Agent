
def test_numba_numeric_colnames(colnames):
    # Check that numeric column names lower properly and can be indexed on
    df = DataFrame(
        np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]], dtype=np.int64), columns=colnames
    )
    first_col = colnames[0]
    f = lambda x: x[first_col]  # Get the first column
    result = df.apply(f, engine="numba", axis=1)
    expected = df.apply(f, engine="python", axis=1)
    tm.assert_series_equal(result, expected)

