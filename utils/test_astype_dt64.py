
def test_astype_dt64():
    # GH#32435
    arr = pd.array([1, 2, 3, pd.NA]) * 10**9

    result = arr.astype("datetime64[ns]")

    expected = np.array([1, 2, 3, "NaT"], dtype="M8[s]").astype("M8[ns]")
    tm.assert_numpy_array_equal(result, expected)

