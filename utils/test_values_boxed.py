
def test_values_boxed():
    tuples = [
        (1, pd.Timestamp("2000-01-01")),
        (2, pd.NaT),
        (3, pd.Timestamp("2000-01-03")),
        (1, pd.Timestamp("2000-01-04")),
        (2, pd.Timestamp("2000-01-02")),
        (3, pd.Timestamp("2000-01-03")),
    ]
    result = MultiIndex.from_tuples(tuples)
    expected = construct_1d_object_array_from_listlike(tuples)
    tm.assert_numpy_array_equal(result.values, expected)
    # Check that code branches for boxed values produce identical results
    tm.assert_numpy_array_equal(result.values[:4], result[:4].values)

