
def test_get_timedelta_field_readonly(dtindex):
    # treat dtindex as timedeltas for this next one
    result = fields.get_timedelta_field(dtindex, "seconds")
    expected = np.array([0] * 5, dtype=np.int32)
    tm.assert_numpy_array_equal(result, expected)

