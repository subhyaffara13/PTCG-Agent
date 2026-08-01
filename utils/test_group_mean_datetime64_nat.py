
def test_group_mean_datetime64_nat(input_data, expected_output):
    # GH43132
    data = to_datetime(Series(input_data))
    expected = to_datetime(Series(expected_output, index=np.array([0])))

    result = data.groupby([0, 0, 0]).mean()
    tm.assert_series_equal(result, expected)

