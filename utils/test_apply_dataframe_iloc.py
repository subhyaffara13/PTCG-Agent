
def test_apply_dataframe_iloc():
    uintDF = DataFrame(np.uint64([1, 2, 3, 4, 5]), columns=["Numbers"])
    indexDF = DataFrame([2, 3, 2, 1, 2], columns=["Indices"])

    def retrieve(targetRow, targetDF):
        val = targetDF["Numbers"].iloc[targetRow]
        return val

    result = indexDF["Indices"].apply(retrieve, args=(uintDF,))
    expected = Series([3, 4, 3, 2, 3], name="Indices", dtype="uint64")
    tm.assert_series_equal(result, expected)

