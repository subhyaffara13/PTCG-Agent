
def test_reindex_periodindex_with_object(p_values, o_values, values, expected_values):
    # GH#28337
    period_index = PeriodIndex(p_values)
    object_index = Index(o_values)

    ser = Series(values, index=period_index)
    result = ser.reindex(object_index)
    expected = Series(expected_values, index=object_index)
    tm.assert_series_equal(result, expected)

