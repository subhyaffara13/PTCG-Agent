
def test_cython_api2(as_index):
    # this takes the fast apply path

    # cumsum (GH5614)
    # GH 5755 - cumsum is a transformer and should ignore as_index
    df = DataFrame([[1, 2, np.nan], [1, np.nan, 9], [3, 4, 9]], columns=["A", "B", "C"])
    expected = DataFrame([[2, np.nan], [np.nan, 9], [4, 9]], columns=["B", "C"])
    result = df.groupby("A", as_index=as_index).cumsum()
    tm.assert_frame_equal(result, expected)

