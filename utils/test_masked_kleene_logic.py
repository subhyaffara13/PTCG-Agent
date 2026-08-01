
def test_masked_kleene_logic(all_boolean_reductions, skipna, data):
    # GH#37506
    ser = Series(data, dtype="boolean")

    # The result should match aggregating on the whole series. Correctness
    # there is verified in test_reductions.py::test_any_all_boolean_kleene_logic
    expected_data = getattr(ser, all_boolean_reductions)(skipna=skipna)
    expected = Series(expected_data, index=np.array([0]), dtype="boolean")

    result = ser.groupby([0, 0, 0]).agg(all_boolean_reductions, skipna=skipna)
    tm.assert_series_equal(result, expected)

