
def test_masked_bool_aggs_skipna(
    all_boolean_reductions, dtype, skipna, frame_or_series
):
    # GH#40585
    obj = frame_or_series([pd.NA, 1], dtype=dtype)
    expected_res = True
    if not skipna and all_boolean_reductions == "all":
        expected_res = pd.NA
    expected = frame_or_series([expected_res], index=np.array([1]), dtype="boolean")

    result = obj.groupby([1, 1]).agg(all_boolean_reductions, skipna=skipna)
    tm.assert_equal(result, expected)

