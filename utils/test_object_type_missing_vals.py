
def test_object_type_missing_vals(bool_agg_func, data, expected_res, frame_or_series):
    # GH#37501
    obj = frame_or_series(data, dtype=object)
    result = obj.groupby([1] * len(data)).agg(bool_agg_func)
    expected = frame_or_series([expected_res], index=np.array([1]), dtype="bool")
    tm.assert_equal(result, expected)

