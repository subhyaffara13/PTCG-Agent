
def test_apply_empty_list_reduce():
    # GH#35683 get columns correct
    df = DataFrame([[1, 2], [3, 4], [5, 6], [7, 8], [9, 10]], columns=["a", "b"])

    result = df.apply(lambda x: [], result_type="reduce")
    expected = Series({"a": [], "b": []}, dtype=object)
    tm.assert_series_equal(result, expected)

