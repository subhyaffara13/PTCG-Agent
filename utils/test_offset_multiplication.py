
def test_offset_multiplication(
    n_months, scaling_factor, start_timestamp, expected_timestamp
):
    # GH 47953
    mo1 = DateOffset(months=n_months)

    startscalar = Timestamp(start_timestamp)
    startarray = Series([startscalar])

    resultscalar = startscalar + (mo1 * scaling_factor)
    resultarray = startarray + (mo1 * scaling_factor)

    expectedscalar = Timestamp(expected_timestamp)
    expectedarray = Series([expectedscalar])
    assert resultscalar == expectedscalar

    tm.assert_series_equal(resultarray, expectedarray)

