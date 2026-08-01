
def test_duplicated_categorical_bool_na(nulls_fixture):
    # GH#44351
    ser = Series(
        Categorical(
            [True, False, True, False, nulls_fixture],
            categories=[True, False],
            ordered=True,
        )
    )
    result = ser.duplicated()
    expected = Series([False, False, True, True, False])
    tm.assert_series_equal(result, expected)

